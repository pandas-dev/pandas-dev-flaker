import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF001 found import from 'collections.abc' "
    "(use 'from collections import abc')"
)


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module is not None and node.module.split(".")[:2] == [
        "collections",
        "abc",
    ]:
        yield node.lineno, node.col_offset, MSG


@register(ast.Import)
def visit_Import(
    state: State,
    node: ast.Import,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if ["collections", "abc"] in [
        name.name.split(".")[:2] for name in node.names
    ]:
        yield node.lineno, node.col_offset, MSG
