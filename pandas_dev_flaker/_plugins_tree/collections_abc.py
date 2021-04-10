import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF001 don't import from collections.abc"


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "collections.abc":
        yield node.lineno, node.col_offset, MSG
