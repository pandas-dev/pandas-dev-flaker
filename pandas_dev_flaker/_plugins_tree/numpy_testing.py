import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF025 found 'np.testing' or 'np.array_equal' "
    "(use 'pandas._testing' instead)"
)


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        (
            "testing" in {name.name for name in node.names}
            or "array_equal" in {name.name for name in node.names}
        )
        and node.module is not None
        and node.module == "numpy"
    ) or (node.module is not None and node.module == "numpy.testing"):
        yield node.lineno, node.col_offset, MSG


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr in {"testing", "array_equal"}
        and isinstance(node.value, ast.Name)
        and node.value.id in {"numpy", "np"}
    ):
        yield node.lineno, node.col_offset, MSG
