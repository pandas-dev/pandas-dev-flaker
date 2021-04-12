import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF017 'pd.api.types' used (import from 'pandas.api.types' instead)"


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
