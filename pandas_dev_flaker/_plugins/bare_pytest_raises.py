import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data import State, register

MSG = "PSG010 bare pytest raises found"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if not node.keywords:
        yield node.lineno, node.col_offset, MSG
    elif "match" not in {keyword.arg for keyword in node.keywords}:
        yield node.lineno, node.col_offset, MSG
