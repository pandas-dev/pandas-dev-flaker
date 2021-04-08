import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

PRIVATE_FUNCTIONS_ALLOWED = {"sys._getframe"}  # no known alternative

MSG = 'PSG010 private import!'
@register(ast.Call)
def np_bool_object(state, node, parent):
    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and (
        any(node.func.value.id in imports for imports in state.from_imports.values())
        or   
        any(node.func.value.id in imports for imports in state.from_imports)
     ) and node.func.attr.startswith('_'):
        yield node.lineno, node.col_offset, MSG
