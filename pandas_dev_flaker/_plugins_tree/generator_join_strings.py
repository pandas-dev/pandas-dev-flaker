"""
Based on

https://github.com/asottile/pyupgrade/blob/5fb168667ae73f157dd579344708e1cdfb0c0341/pyupgrade/_plugins/generator_expressions_pep289.py
"""

import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import is_str_constant
from pandas_dev_flaker._data_tree import State, register

MSG = "PDF024 found string join() with generator expressions"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "join"
        and is_str_constant(node)
        and node.args
        and isinstance(node.args[0], ast.GeneratorExp)
    ):
        yield (node.lineno, node.col_offset, MSG)
