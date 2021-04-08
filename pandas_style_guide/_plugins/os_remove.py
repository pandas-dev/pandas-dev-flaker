import ast
from typing import Iterator, Tuple

from pandas_style_guide._ast_helpers import is_name_attr
from pandas_style_guide._data import State, register

MSG = "PSG010 os remove"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        is_name_attr(
            node.func,
            state.from_imports,
            "os",
            ("remove",),
        )
        and not isinstance(parent, ast.withitem)
    ):
        yield node.lineno, node.col_offset, MSG
    elif (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "remove"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "os"
        and not isinstance(parent, ast.withitem)
    ):
        yield node.lineno, node.col_offset, MSG
