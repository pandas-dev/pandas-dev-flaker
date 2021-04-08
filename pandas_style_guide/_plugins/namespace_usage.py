
import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 namespace inconsistency'
@register(ast.Attribute)
def visit_Attribute(state, node: ast.Attribute, parent) -> None:
    if node.attr in state.from_imports['pandas'] and isinstance(node.value, ast.Name) and node.value.id in {'pandas', 'pd'}:
        yield node.lineno, node.col_offset, MSG