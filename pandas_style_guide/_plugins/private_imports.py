import ast
from typing import Iterator, Tuple

from pandas_style_guide._data import State, register

PRIVATE_FUNCTIONS_ALLOWED = {"sys._getframe"}  # no known alternative

MSG = "PSG010 private import!"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and (
            any(
                node.func.value.id in imports
                for imports in state.from_imports.values()
            )
            or any(
                node.func.value.id in imports for imports in state.from_imports
            )
        )
        and node.func.attr.startswith("_")
    ):
        yield node.lineno, node.col_offset, MSG
