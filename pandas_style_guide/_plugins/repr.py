import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG007 Don\'t use !r, use repr'
@register(ast.FormattedValue)
def dont_use_formatted_repr(state, node, parent):
    if node.conversion == 114:
        yield node.lineno, node.col_offset, MSG