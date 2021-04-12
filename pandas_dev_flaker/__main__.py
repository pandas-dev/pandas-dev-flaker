import ast
import tokenize
from typing import Iterator, Sequence, Tuple

import pkg_resources

from pandas_dev_flaker._data_tokens import FUNCS_TOKENS, visit_tokens
from pandas_dev_flaker._data_tree import FUNCS_TREE, visit_tree

pkg_name = "pandas-dev-flaker"

pkg_version: str = pkg_resources.get_distribution(pkg_name).version


def run(
    tree: ast.Module,
    file_tokens: Sequence[tokenize.TokenInfo],
) -> Iterator[Tuple[int, int, str, str]]:
    callbacks_tree = visit_tree(FUNCS_TREE, tree)
    if not callbacks_tree:
        return
    for line, col, msg in callbacks_tree:
        yield line, col, msg, "pandas_dev_flaker"

    callbacks_tokens = visit_tokens(FUNCS_TOKENS, file_tokens)
    if not callbacks_tokens:
        return
    for line, col, msg in callbacks_tokens:
        yield line, col, msg, "pandas_dev_flaker"


run.name = pkg_name  # type: ignore
run.version = pkg_version  # type: ignore
