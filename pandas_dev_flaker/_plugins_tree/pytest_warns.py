import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF011 found 'pytest.warns' "
    "(use 'pandas._testing.assert_produces_warning')"
)


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "warns"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "pytest"
    ):
        yield node.lineno, node.col_offset, MSG


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pytest" and "warns" in {
        name.name for name in node.names
    }:
        yield node.lineno, node.col_offset, MSG
