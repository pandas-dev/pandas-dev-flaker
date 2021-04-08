import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG008 don\'t use .__class__, use type()'
@register(ast.Attribute)
def dunder_class(state, node, parent):
    if node.attr == '__class__':
        yield node.lineno, node.col_offset, MSG