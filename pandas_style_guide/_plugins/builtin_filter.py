import ast
from typing import Iterator, Tuple

from pandas_style_guide._data import State, register

MSG = "PSG004 do not use builtin filter function"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if isinstance(node.func, ast.Name):
        if node.func.id == "filter":
            yield (node.lineno, node.col_offset, MSG)
