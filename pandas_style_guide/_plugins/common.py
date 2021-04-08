import ast
from typing import Iterator, Tuple

from pandas_style_guide._data import State, register

MSG = "PSG010 don't import from pandas.core or from pandas.core.common"


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module in {"pandas.core.common", "pandas.core"}:
        yield node.lineno, node.col_offset, MSG
