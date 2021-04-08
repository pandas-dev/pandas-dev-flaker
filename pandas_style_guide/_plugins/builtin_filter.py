import ast
from pandas_style_guide._data import register

MSG = 'PSG004 do not use builtin filter function'
@register(ast.Call)
def builtin_filter(state, node, parent):
    if isinstance(node.func, ast.Name):
        if node.func.id == 'filter':
            yield (node.lineno, node.col_offset, MSG)
