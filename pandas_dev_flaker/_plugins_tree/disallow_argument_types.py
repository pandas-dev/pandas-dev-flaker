import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF026 found union between Series and AnyArrayLike in type hint"
SERIES, ANY_ARRAY_LIKE = "Series", "AnyArrayLike"


def _contains_series_and_arraylike(node: ast.AST) -> bool:
    ret = False
    for node in ast.walk(node):
        if isinstance(node, ast.BinOp):
            ret |= _binop_contains_series_and_arraylike(node)
    return ret


def _binop_contains_series_and_arraylike(node: ast.BinOp) -> bool:
    is_series, is_array_like = False, False

    for _node in ast.walk(node):
        if isinstance(_node, ast.Name):
            if _node.id == SERIES:
                is_series = True
            elif _node.id == ANY_ARRAY_LIKE:
                is_array_like = True
        elif isinstance(_node, ast.Str):
            if _node.s == SERIES:
                is_series = True
            elif _node.s == ANY_ARRAY_LIKE:
                is_array_like = True

    return is_series and is_array_like


# for function arguments/returns annotations
@register(ast.FunctionDef)
def visit_FunctionDef(
    state: State,
    node: ast.FunctionDef,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    arguments = node.args.args
    for arg in arguments:
        if arg.annotation is not None and _contains_series_and_arraylike(
            arg.annotation,
        ):
            yield arg.lineno, arg.col_offset, MSG
    if node.returns is not None and _contains_series_and_arraylike(
        node.returns,
    ):
        yield node.lineno, node.col_offset, MSG


# for annotations defined outside function args & return args
@register(ast.AnnAssign)
def visit_AnnAssign(
    state: State,
    node: ast.AnnAssign,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    annotation = node.annotation
    if annotation is not None and _contains_series_and_arraylike(annotation):
        yield node.lineno, node.col_offset, MSG
