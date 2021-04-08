import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 os remove'
@register(ast.Call)
def check_contextless_pytest_raises(state, node, parent):
    if is_name_attr(node.func, state.from_imports, 'os', ('remove', )) and not isinstance(parent, ast.withitem):
        yield node.lineno, node.col_offset, MSG
    elif isinstance(node.func, ast.Attribute) and node.func.attr == 'remove' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'os' and not isinstance(parent, ast.withitem):
        yield node.lineno, node.col_offset, MSG
