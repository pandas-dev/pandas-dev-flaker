import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 don\'t import from pandas.core or from pandas.core.common'
@register(ast.ImportFrom)
def np_bool_object(state, node, parent):
    if node.module in {'pandas.core.common', 'pandas.core'}:
        yield node.lineno, node.col_offset, MSG