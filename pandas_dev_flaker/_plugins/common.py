import ast
from typing import Iterator, Sequence, Tuple

from pandas_dev_flaker._data import State, register

MSG = "PDF009 don't import from pandas.core or from pandas.core.common"


def _check_for_wrong_alias(
    names: Sequence[ast.alias],
    name: str,
    alias: str,
) -> bool:
    for name_ in names:
        if name_.name == name:
            return name_.asname == alias
    else:
        return False


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pandas.core.common" or (
        node.module == "pandas.core"
        and _check_for_wrong_alias(node.names, "common", "comm")
    ):
        yield node.lineno, node.col_offset, MSG
