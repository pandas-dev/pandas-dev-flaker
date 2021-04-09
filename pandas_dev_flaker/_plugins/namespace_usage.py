import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data import State, register

MSG = "PDF012 namespace inconsistency"


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr in state.from_imports["pandas"]
        and isinstance(node.value, ast.Name)
        and node.value.id in {"pandas", "pd"}
    ):
        yield node.lineno, node.col_offset, MSG
