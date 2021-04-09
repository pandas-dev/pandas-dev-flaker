import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data import State, register

PRIVATE_FUNCTIONS_ALLOWED = {"sys._getframe"}  # no known alternative

MSG = "PDF018 private import!"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and not node.func.value.id[0].isupper()
        and not (
            node.func.value.id.startswith("__")
            and node.func.value.id.endswith("__")
        )
        and (
            any(
                node.func.value.id in imports
                for imports in state.from_imports.values()
            )
            or node.func.value.id in state.from_imports
        )
        and node.func.attr.startswith("_")
        and f"{node.func.value.id}.{node.func.attr}"
        not in PRIVATE_FUNCTIONS_ALLOWED
    ):
        yield node.lineno, node.col_offset, MSG
