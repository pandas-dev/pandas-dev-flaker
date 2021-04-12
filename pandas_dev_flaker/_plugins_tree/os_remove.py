import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import is_name_attr
from pandas_dev_flaker._data_tree import State, register

MSG = "PDF008 found 'os.remove' (use 'tm.ensure_clean' instead)"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if is_name_attr(
        node.func,
        state.from_imports,
        "os",
        ("remove",),
    ):
        yield node.lineno, node.col_offset, MSG
