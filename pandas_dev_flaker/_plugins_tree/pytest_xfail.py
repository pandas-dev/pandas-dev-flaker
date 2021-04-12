import ast
import sys
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF012 found 'pytest.xfail' (use 'pytest.mark.xfail' instead)"


@register(ast.FunctionDef)
def visit_FunctionDef(
    state: State,
    node: ast.FunctionDef,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    for decorator in node.decorator_list:
        if (
            isinstance(decorator, ast.Attribute)
            and decorator.attr == "xfail"
            and isinstance(decorator.value, ast.Name)
            and decorator.value.id == "pytest"
        ):
            if sys.version_info >= (3, 8):  # pragma: no cover (<py38)
                yield node.lineno, node.col_offset, MSG
            else:  # pragma: no cover (py38+)
                yield node.lineno + 1, node.col_offset, MSG


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pytest" and "xfail" in {
        name.name for name in node.names
    }:
        yield node.lineno, node.col_offset, MSG
