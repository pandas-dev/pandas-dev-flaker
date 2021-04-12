import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF004 'foo.__class__' used, (use 'type(foo)' instead)"


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.attr == "__class__":
        yield node.lineno, node.col_offset, MSG
