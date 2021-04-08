import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG009 don\'t use numpy.bool or numpy.object but numpy.bool_ and numpy.object_'
@register(ast.Name)
def np_bool_object(state, node, parent):
    if is_name_attr(node, state.from_imports, 'numpy', ('bool', 'object', )):
        yield node.lineno, node.col_offset, MSG

@register(ast.Attribute)
def np_bool_object(state, node, parent):
    if node.attr in {'bool', 'object'} and isinstance(node.value, ast.Name) and node.value.id in {'numpy', 'np'}:
        yield node.lineno, node.col_offset, MSG
