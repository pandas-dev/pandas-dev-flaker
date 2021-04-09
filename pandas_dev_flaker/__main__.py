import ast
import importlib.metadata
import os
from typing import Any, Generator, Tuple, Type

from pandas_dev_flaker._data import FUNCS, visit


class Plugin:
    name = os.path.split(os.path.dirname(__file__))[-1]
    version = importlib.metadata.version(name)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        callbacks = visit(FUNCS, self._tree)
        if not callbacks:
            return
        for line, col, msg in callbacks:
            yield line, col, msg, type(self)
