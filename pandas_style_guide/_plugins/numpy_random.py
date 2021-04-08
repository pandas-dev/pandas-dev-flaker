import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 don\'t import numpy.random'
@register(ast.ImportFrom)
def abc(state, node, parent):
    if node.module == 'numpy.random' or (node.module == 'numpy' and 'random' in {name.name for name in node.names}):
        yield node.lineno, node.col_offset, MSG
