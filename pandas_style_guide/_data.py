import pkgutil
import collections
from typing import List, Tuple, Dict, NamedTuple, Set
import ast
from pandas_style_guide import _plugins

FUNCS = collections.defaultdict(list)
RECORD_FROM_IMPORTS = frozenset((
    'pytest',
))
class State(NamedTuple):
    from_imports: Dict[str, Set[str]]
    in_annotation: bool = False

def register(tp):
    def register_decorator(func):
        FUNCS[tp].append(func)
        return func
    return register_decorator


def visit(funcs, tree: ast.Module) -> Dict[int, List[int]]:
    "Step through tree, recording when nodes are in annotations."
    initial_state = State(
        from_imports=collections.defaultdict(set),
    )
    nodes: List[Tuple[bool, ast.AST, ast.AST]] = [(initial_state, tree, tree)]

    while nodes:
        state, node, parent = nodes.pop()
        tp = type(node)
        for ast_func in funcs[tp]:
            yield from ast_func(state, node, parent)

        if (
                isinstance(node, ast.ImportFrom) and
                not node.level and
                node.module in RECORD_FROM_IMPORTS
        ):
            state.from_imports[node.module].update(
                name.name for name in node.names if not name.asname
            )

        for name in reversed(node._fields):
            value = getattr(node, name)
            if name in {"annotation", "returns"}:
                next_in_annotation = True
            else:
                next_in_annotation = state
            if isinstance(value, ast.AST):
                nodes.append((next_in_annotation, value, node))
            elif isinstance(value, list):
                for value in reversed(value):
                    if isinstance(value, ast.AST):
                        nodes.append((next_in_annotation, value, node))

def _import_plugins() -> None:
    # https://github.com/python/mypy/issues/1422
    plugins_path: str = _plugins.__path__  # type: ignore
    mod_infos = pkgutil.walk_packages(plugins_path, f'{_plugins.__name__}.')
    for _, name, _ in mod_infos:
        __import__(name, fromlist=['_trash'])


_import_plugins()