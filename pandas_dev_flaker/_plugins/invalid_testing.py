import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data import State, register

MSG = "PSG005 don't use np.testing or np.array_equal"


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr in {"testing", "array_equal"}
        and isinstance(node.value, ast.Name)
        and node.value.id in {"np", "numpy"}
    ):
        yield node.lineno, node.col_offset, MSG
