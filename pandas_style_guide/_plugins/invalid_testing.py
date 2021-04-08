import ast
from pandas_style_guide._data import register

MSG = 'PSG005 don\'t use np.testing or np.array_equal'
@register(ast.Attribute)
def check_for_pytest_warns(state, node, parent):
    if node.attr in {'testing', 'array_equal'} and isinstance(node.value, ast.Name) and  node.value.id in {'np', 'numpy'}  :
        yield node.lineno, node.col_offset, MSG
