import ast
from pandas_style_guide._data import register

MSG = 'PSG002 do not use pytest.warns'
@register(ast.Attribute)
def check_for_pytest_warns(self, node):
    if node.value.id == 'pytest' and node.attr == 'warns':
        yield node.lineno, node.col_offset, MSG