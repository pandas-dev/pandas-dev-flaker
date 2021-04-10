import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF020 Don't use !r, use repr"


@register(ast.FormattedValue)
def visit_FormattedValue(
    state: State,
    node: ast.FormattedValue,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.conversion == 114:
        yield node.lineno, node.col_offset, MSG
