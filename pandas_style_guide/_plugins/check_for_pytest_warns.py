import ast
from pandas_style_guide._data import register

MSG = 'PSG002 do not use pytest.warns'
@register(ast.Attribute)
def check_for_pytest_warns(state, node, parent):
    if node.attr == 'warns' and isinstance(node.value, ast.Name) and node.value.id == 'pytest' :
        yield node.lineno, node.col_offset, MSG