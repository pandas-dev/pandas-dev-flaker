import pkgutil
import tokenize
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Sequence,
    Set,
    Tuple,
)

if TYPE_CHECKING:
    from typing import Protocol
else:
    Protocol = object

from pandas_dev_flaker import _plugins_tokens


class State(NamedTuple):
    from_imports: Dict[str, Set[str]]
    in_annotation: bool = False


TokensFunc = Callable[
    [Sequence[tokenize.TokenInfo]],
    Iterable[Tuple[int, int, str]],
]


FUNCS_TOKENS = []


def register() -> Callable[[TokensFunc], TokensFunc]:
    def register_decorator(func: TokensFunc) -> TokensFunc:
        FUNCS_TOKENS.append(func)
        return func

    return register_decorator


def visit_tokens(
    funcs: List[TokensFunc],
    tokens: Sequence[tokenize.TokenInfo],
) -> Iterator[Tuple[int, int, str]]:
    "Step through tree, recording when nodes are in annotations."
    for token_func in funcs:
        yield from token_func(tokens)


def _import_plugins() -> None:
    # https://github.com/python/mypy/issues/1422
    plugins_path: str = _plugins_tokens.__path__  # type: ignore
    mod_infos = pkgutil.walk_packages(
        plugins_path,
        f"{_plugins_tokens.__name__}.",
    )
    for _, name, _ in mod_infos:
        __import__(name, fromlist=["_trash"])


_import_plugins()
