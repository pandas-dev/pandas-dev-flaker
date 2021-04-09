import ast
import os
import sys
from typing import Any, Generator, Tuple, Type

from pandas_dev_flaker._data import FUNCS, visit

if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    import importlib_metadata
else:  # pragma: no cover (PY38+)
    import importlib.metadata as importlib_metadata


class Plugin:
    name = os.path.split(os.path.dirname(__file__))[-1]
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        callbacks = visit(FUNCS, self._tree)
        if not callbacks:
            return
        for line, col, msg in callbacks:
            yield line, col, msg, type(self)
