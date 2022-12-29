import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF023 found assignment to single-letter variable"


@register(ast.Assign)
def visit_Assign(
    state: State,
    node: ast.Assign,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:

    # Unpacking is represented by putting a Tuple or List within targets
    if isinstance(node.targets[0], (ast.Tuple, ast.List)):
        assignment_names = node.targets[0].elts
    else:
        assignment_names = node.targets

    for item in assignment_names:
        if isinstance(item, ast.Name) and item.id != "_" and len(item.id) == 1:
            yield item.lineno, item.col_offset, MSG
