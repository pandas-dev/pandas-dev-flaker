import collections
from typing import List, Tuple, Dict
import ast

FUNCS = collections.defaultdict(list)
def register(tp):
    def register_decorator(func):
        FUNCS[tp].append(func)
        return func
    return register_decorator


def visit(funcs, tree: ast.Module) -> Dict[int, List[int]]:
    "Step through tree, recording when nodes are in annotations."
    in_annotation = False
    nodes: List[Tuple[bool, ast.AST]] = [(in_annotation, tree)]

    while nodes:
        in_annotation, node = nodes.pop()

        tp = type(node)
        for ast_func in funcs[tp]:
            yield from ast_func(in_annotation, node)

        for name in reversed(node._fields):
            value = getattr(node, name)
            if name in {"annotation", "returns"}:
                next_in_annotation = True
            else:
                next_in_annotation = in_annotation
            if isinstance(value, ast.AST):
                nodes.append((next_in_annotation, value))
            elif isinstance(value, list):
                for value in reversed(value):
                    if isinstance(value, ast.AST):
                        nodes.append((next_in_annotation, value))

