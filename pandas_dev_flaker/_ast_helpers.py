import ast
from typing import Container, Dict, Set


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
