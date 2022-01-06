import ast
import sys
from typing import Container, Dict, Sequence, Set


def is_name_attr(
    node: ast.AST,
    imports: Dict[str, Set[str]],
    mod: str,
    names: Container[str],
) -> bool:
    return (
        isinstance(node, ast.Name)
        and node.id in names
        and node.id in imports[mod]
    ) or (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == mod
        and node.attr in names
    )


def check_for_wrong_alias(
    names: Sequence[ast.alias],
    name: str,
    alias: str,
) -> bool:
    for name_ in names:
        if name_.name == name:
            return name_.asname != alias
    else:
        return False


def is_str_constant(
    node: ast.Call,
) -> bool:
    return isinstance(node.func, ast.Attribute) and (
        (sys.version_info < (3, 8) and isinstance(node.func.value, ast.Str))
        or (
            sys.version_info >= (3, 8)
            and isinstance(node.func.value, ast.Constant)
            and isinstance(node.func.value.value, str)
        )
    )
