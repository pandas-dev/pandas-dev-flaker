import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import is_name_attr
from pandas_dev_flaker._data_tree import State, register

MSG = "PDF009 'pytest.raises' used without 'match='"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "raises"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "pytest"
    ) or is_name_attr(
        node.func,
        state.from_imports,
        "pytest",
        ("raises",),
    ):
        if not node.keywords:
            yield node.lineno, node.col_offset, MSG
        elif "match" not in {keyword.arg for keyword in node.keywords}:
            yield node.lineno, node.col_offset, MSG
