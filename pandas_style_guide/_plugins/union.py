
import ast
from pandas_style_guide._data import register
from pandas_style_guide._ast_helpers import is_name_attr

MSG = 'PSG010 union'

@register(ast.Subscript)
def visit_Subscript(state, node, parent):
    if isinstance(node.value, ast.Name) and node.value.id == 'Union':
        if isinstance(node.slice, ast.Index):
            tuple = node.slice.value
        else:
            tuple = node.slice
        names = set()
        if isinstance(tuple, ast.Tuple):
            for elt in tuple.elts:
                if isinstance(elt, ast.Name):
                    names.add(elt.id)
        if names == {'DataFrame', 'Series'}:
            yield node.lineno, node.col_offset, MSG
