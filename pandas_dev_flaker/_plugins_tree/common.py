import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import check_for_wrong_alias
from pandas_dev_flaker._data_tree import State, register

MSG = "PDF018 'common' imported from 'pandas.core' without 'com' alias"


@register(ast.Import)
def visit_Import(
    state: State,
    node: ast.Import,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if check_for_wrong_alias(node.names, "pandas.core.common", "com"):
        yield node.lineno, node.col_offset, MSG


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pandas.core.common" or (
        node.module == "pandas.core"
        and check_for_wrong_alias(node.names, "common", "com")
    ):
        yield node.lineno, node.col_offset, MSG
