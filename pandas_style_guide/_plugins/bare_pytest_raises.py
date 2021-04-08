import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 bare pytest raises found'
@register(ast.Call)
def np_bool_object(state, node, parent):
    if not node.keywords:
        yield node.lineno, node.col_offset, MSG
    elif 'match' not in {keyword.arg for keyword in node.keywords}:
        yield node.lineno, node.col_offset, MSG
