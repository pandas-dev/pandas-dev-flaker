import ast
import collections
import pkgutil
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Set,
    Tuple,
    Type,
    TypeVar,
)

if TYPE_CHECKING:
    from typing import Protocol
else:
    Protocol = object

from pandas_dev_flaker import _plugins_tree


class State(NamedTuple):
    from_imports: Dict[str, Set[str]]
    in_annotation: bool = False


AST_T = TypeVar("AST_T", bound=ast.AST)
ASTFunc = Callable[[State, AST_T, ast.AST], Iterable[Tuple[int, int, str]]]


FUNCS_TREE = collections.defaultdict(list)


class ASTCallbackMapping(Protocol):
    def __getitem__(self, tp: Type[AST_T]) -> List[ASTFunc[AST_T]]:
        ...


def register(
    tp: Type[AST_T],
) -> Callable[[ASTFunc[AST_T]], ASTFunc[AST_T]]:
    def register_decorator(func: ASTFunc[AST_T]) -> ASTFunc[AST_T]:
        FUNCS_TREE[tp].append(func)
        return func

    return register_decorator


def _get_alias(name: ast.alias) -> str:
    if name.asname is not None:
        return name.asname
    else:
        return name.name


def visit_tree(
    funcs: ASTCallbackMapping,
    tree: ast.Module,
) -> Iterator[Tuple[int, int, str]]:
    "Step through tree, recording when nodes are in annotations."
    initial_state = State(
        from_imports=collections.defaultdict(set),
    )
    nodes: List[Tuple[State, ast.AST, ast.AST]] = [(initial_state, tree, tree)]

    while nodes:
        state, node, parent = nodes.pop()
        tp = type(node)
        for ast_func in funcs[tp]:
            yield from ast_func(state, node, parent)

        if isinstance(node, ast.ImportFrom) and node.module is not None:
            state.from_imports[node.module.split(".")[0]].update(
                _get_alias(name) for name in node.names if not name.asname
            )
        elif isinstance(node, ast.Import):
            for node_name in node.names:
                state.from_imports[_get_alias(node_name)]

        for name in reversed(node._fields):
            value = getattr(node, name)
            if name in {"annotation", "returns"}:
                next_state = state._replace(in_annotation=True)
            else:
                next_state = state
            if isinstance(value, ast.AST):
                nodes.append((next_state, value, node))
            elif isinstance(value, list):
                for value in reversed(value):
                    if isinstance(value, ast.AST):
                        nodes.append((next_state, value, node))


def _import_plugins() -> None:
    # https://github.com/python/mypy/issues/1422
    plugins_path: str = _plugins_tree.__path__  # type: ignore
    mod_infos = pkgutil.walk_packages(
        plugins_path,
        f"{_plugins_tree.__name__}.",
    )
    for _, name, _ in mod_infos:
        __import__(name, fromlist=["_trash"])


_import_plugins()
