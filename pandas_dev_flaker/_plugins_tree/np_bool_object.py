import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF021 found 'np.bool' or 'np.object' "
    "(use 'np.bool_' or 'np.object_' instead)"
)


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        (
            "object" in {name.name for name in node.names}
            or "bool" in {name.name for name in node.names}
        )
        and node.module is not None
        and node.module == "numpy"
    ):
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
