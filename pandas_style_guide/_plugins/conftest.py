import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 Don\'t import from conftest'
@register(ast.ImportFrom)
def abc(state, node, parent):
    if node.module == 'conftest':
        yield node.lineno, node.col_offset, MSG

@register(ast.Import)
def abc(state, node, parent):
    if 'conftest' in {name.name for name in node.names}:
        yield node.lineno, node.col_offset, MSG
