import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = (
    "PDF015 found import from 'pandas.testing' "
    "(use 'import pandas._testing as tm')"
)


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.module == "pandas"
        and "testing" in {name.name for name in node.names}
    ) or (
        node.module is not None
        and node.module.split(".")[:2] == ["pandas", "testing"]
    ):
        yield node.lineno, node.col_offset, MSG


@register(ast.Import)
def visit_Import(
    state: State,
    node: ast.Import,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if "pandas.testing" in {name.name for name in node.names}:
        yield node.lineno, node.col_offset, MSG


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if isinstance(node.value, ast.Name) and (
        (node.attr == "testing" and node.value.id in {"pandas", "pd"})
        or node.value.id.split(".")[:2]
        in [["pd", "testing"], ["pandas", "testing"]]
    ):
        yield node.lineno, node.col_offset, MSG
