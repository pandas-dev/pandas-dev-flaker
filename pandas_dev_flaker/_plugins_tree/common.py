import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import check_for_wrong_alias
from pandas_dev_flaker._data_tree import State, register

MSG = "PDF009 'common' imported from 'pandas.core' without 'comm' alias"


@register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if node.module == "pandas.core.common" or (
        node.module == "pandas.core"
        and check_for_wrong_alias(node.names, "common", "comm")
    ):
        yield node.lineno, node.col_offset, MSG
