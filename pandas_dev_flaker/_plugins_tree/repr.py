import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF006 Found '{foo!r}' formatted value (instead, use 'repr(foo)')"


@register(ast.FormattedValue)
def visit_FormattedValue(
    state: State,
    node: ast.FormattedValue,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.conversion == 114:
        yield node.lineno, node.col_offset, MSG
