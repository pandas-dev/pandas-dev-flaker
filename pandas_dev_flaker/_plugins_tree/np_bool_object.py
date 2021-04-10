import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import is_name_attr
from pandas_dev_flaker._data_tree import State, register

MSG = "PDF013 don't use np.bool or np.object but np.bool_ and np.object_"


@register(ast.Name)
def visit_Name(
    state: State,
    node: ast.Name,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if is_name_attr(node, state.from_imports, "numpy", ("bool", "object")):
        yield node.lineno, node.col_offset, MSG


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr in {"bool", "object"}
        and isinstance(node.value, ast.Name)
        and node.value.id in {"numpy", "np"}
    ):
        yield node.lineno, node.col_offset, MSG
