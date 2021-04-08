import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG006 do not use unitest.mock, use pytest\'s monkeypatch'
@register(ast.Name)
def check_for_pytest_warns(state, node, parent):
    if is_name_attr(node, state.from_imports, 'unittest', ('mock', )):
        yield node.lineno, node.col_offset, MSG

@register(ast.Attribute)
def check_for_pytest_warns(state, node, parent):
    if node.attr == 'mock' and isinstance(node.value, ast.Name) and node.value.id == 'unittest':
        yield node.lineno, node.col_offset, MSG
