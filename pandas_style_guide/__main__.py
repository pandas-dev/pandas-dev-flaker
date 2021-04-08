from __future__ import annotations
import tokenize


import ast
import importlib.metadata
from typing import Any, List, Dict, Tuple, Type, Callable
import collections
from typing import Generator

from pandas_style_guide._data import FUNCS, visit




class Plugin:
    name = __name__
    version = 1#importlib.metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        callbacks = visit(FUNCS, self._tree)
        if not callbacks:
            return
        for line, col, msg in callbacks:
            yield line, col, msg, type(self)
        