from __future__ import annotations

import argparse
import ast
import tokenize
from io import StringIO
from typing import Iterator, Sequence

import pkg_resources

from pandas_dev_flaker._data_tokens import FUNCS_TOKENS, visit_tokens
from pandas_dev_flaker._data_tree import FUNCS_TREE, visit_tree

pkg_name = "pandas-dev-flaker"

pkg_version: str = pkg_resources.get_distribution(pkg_name).version


def run(
    tree: ast.Module,
    file_tokens: Sequence[tokenize.TokenInfo],
) -> Iterator[tuple[int, int, str, str]]:
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


def run_flaker(path: str) -> int:  # pragma: no cover
    try:
        with open(path, encoding="utf-8") as fd:
            content = fd.read()
    except UnicodeDecodeError:
        # Don't parse non-utf8
        return 0
    try:
        tree = ast.parse(content)
    except (SyntaxError, ValueError):
        # Don't lint garbage
        return 0
    file_tokens = list(tokenize.generate_tokens(StringIO(content).readline))

    callbacks_tree = visit_tree(FUNCS_TREE, tree)
    ret = 0
    if not callbacks_tree:
        pass
    for line, col, msg in callbacks_tree:
        print(f"{path}:{line}:{col}: {msg}")
        ret = 1

    callbacks_tokens = visit_tokens(FUNCS_TOKENS, file_tokens)
    if not callbacks_tokens:
        pass
    for line, col, msg in callbacks_tokens:
        print(f"{path}:{line}:{col}: {msg}")
        ret = 1
    return ret


def main(argv: Sequence[str] | None = None) -> int:  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args(argv)
    ret = 0
    for path in args.paths:
        ret |= run_flaker(path)
    return ret


if __name__ == "__main__":
    main()
