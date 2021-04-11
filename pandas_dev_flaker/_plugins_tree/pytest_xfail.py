import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF015 found pytest.xfail (use pytest.mark.xfail instead)"


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr == "xfail"
        and isinstance(node.value, ast.Name)
        and node.value.id == "pytest"
    ):
        yield node.lineno, node.col_offset, MSG


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pytest" and "xfail" in {
        name.name for name in node.names
    }:
        yield node.lineno, node.col_offset, MSG
