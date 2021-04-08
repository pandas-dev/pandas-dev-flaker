import ast
from typing import Iterator, Tuple

from pandas_style_guide._data import State, register

MSG = "PSG005 dont use pd.api.types, import from pandas.api.types instead"


@register(ast.Attribute)
def check_for_pytest_warns(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.value, ast.Attribute)
        and node.value.attr == "types"
        and isinstance(node.value.value, ast.Attribute)
        and node.value.value.attr == "api"
        and isinstance(node.value.value.value, ast.Name)
        and node.value.value.value.id in {"pd", "pandas"}
    ):
        yield node.lineno, node.col_offset, MSG
