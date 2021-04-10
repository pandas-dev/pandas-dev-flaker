import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF001 import from collections.abc "
    "(use 'from collections import abc' instead)"
)


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "collections.abc":
        yield node.lineno, node.col_offset, MSG


@register(ast.Import)
def visit_Import(
    state: State,
    node: ast.Import,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if "collections.abc" in {name.name for name in node.names}:
        yield node.lineno, node.col_offset, MSG
