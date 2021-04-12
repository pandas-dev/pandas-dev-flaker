import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import check_for_wrong_alias
from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF014 found import from 'pandas._testing' "
    "(use 'import pandas._testing as tm')"
)


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pandas._testing" or (
        node.module == "pandas"
        and check_for_wrong_alias(node.names, "_testing", "tm")
    ):
        yield node.lineno, node.col_offset, MSG


@register(ast.Import)
def visit_Import(
    state: State,
    node: ast.Import,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if check_for_wrong_alias(node.names, "pandas._testing", "tm"):
        yield node.lineno, node.col_offset, MSG
