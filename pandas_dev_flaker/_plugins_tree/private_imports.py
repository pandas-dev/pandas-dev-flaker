import ast
from typing import Iterator, Sequence, Tuple

from pandas_dev_flaker._data_tree import State, register

PRIVATE_FUNCTIONS_ALLOWED = {"sys._getframe"}  # no known alternative

MSG = "PDF016 found private import across modules"


def _is_private_import(module: str, attributes: Sequence[str]) -> bool:
    return (
        not module[0].isupper()
        and not any(
            attribute.startswith("__") and attribute.endswith("__")
            for attribute in attributes
        )
        and any(
            attribute.startswith("_")
            and f"{module}.{attribute}" not in PRIVATE_FUNCTIONS_ALLOWED
            for attribute in attributes
        )
    )


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        isinstance(node.value, ast.Name)
        and (
            any(
                node.value.id in imports
                for imports in state.from_imports.values()
            )
            or node.value.id in state.from_imports
        )
        and _is_private_import(node.value.id, [node.attr])
    ):
        yield node.lineno, node.col_offset, MSG
