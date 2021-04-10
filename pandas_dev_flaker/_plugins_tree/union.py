import ast
from typing import Iterator, Tuple, Union

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF021 union"


@register(ast.Subscript)
def visit_Subscript(
    state: State,
    node: ast.Subscript,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if isinstance(node.value, ast.Name) and node.value.id == "Union":
        if isinstance(node.slice, ast.Index):
            tuple: Union[ast.slice, ast.expr] = node.slice.value
        else:
            tuple = node.slice
        names = set()
        if isinstance(tuple, ast.Tuple):
            for elt in tuple.elts:
                if isinstance(elt, ast.Name):
                    names.add(elt.id)
        if names == {"DataFrame", "Series"}:
            yield node.lineno, node.col_offset, MSG
