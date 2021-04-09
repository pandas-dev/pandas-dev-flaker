import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data import State, register

MSG = "PDF007 'pytest.warns' used (use 'tm.assert_produces_warning' instead)"


@register(ast.Attribute)
def check_for_pytest_warns(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr == "warns"
        and isinstance(node.value, ast.Name)
        and node.value.id == "pytest"
    ):
        yield node.lineno, node.col_offset, MSG
