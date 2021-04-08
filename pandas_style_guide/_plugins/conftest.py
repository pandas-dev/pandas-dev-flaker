import ast
from typing import Iterator, Tuple

from pandas_style_guide._data import State, register

MSG = "PSG010 Don't import from conftest"


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "conftest":
        yield node.lineno, node.col_offset, MSG


@register(ast.Import)
def visit_Import(
    state: State,
    node: ast.Import,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if "conftest" in {name.name for name in node.names}:
        yield node.lineno, node.col_offset, MSG
