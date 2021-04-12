import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF016 found 'unittest.mock' (use 'pytest.monkeypatch' instead)"


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        (
            node.module == "unittest"
            and "mock" in {name.name for name in node.names}
        )
        or node.module is not None
        and node.module.split(".")[:2] == ["unittest", "mock"]
    ):
        yield node.lineno, node.col_offset, MSG


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        node.attr == "mock"
        and isinstance(node.value, ast.Name)
        and node.value.id == "unittest"
    ):
        yield node.lineno, node.col_offset, MSG
