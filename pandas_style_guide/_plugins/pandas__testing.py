import ast
from typing import Iterator, Tuple

from pandas_style_guide._data import State, register

MSG = "PSG010 import pandas._testing as tm"


@register(ast.ImportFrom)
def abc(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pandas._testing" or (
        node.module == "numpy"
        and "_testing" in {name.name for name in node.names}
    ):
        yield node.lineno, node.col_offset, MSG
