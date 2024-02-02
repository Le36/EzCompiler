import compiler.src.ast as ast
from dataclasses import dataclass, field, is_dataclass, fields
from typing import Any, List


def ast_equal(node1: Any, node2: Any, path: str = '') -> str:
    errors = []

    if not isinstance(node1, type(node2)):
        return f'Node type mismatch at {path}: {type(node1).__name__} != {type(node2).__name__}'

    if is_dataclass(node1):
        for f in fields(node1):
            field1 = getattr(node1, f.name)
            field2 = getattr(node2, f.name)
            result = ast_equal(field1, field2, path=f'{path}.{f.name}')
            if result:
                errors.append(result)
    elif isinstance(node1, list) and isinstance(node2, list):
        if len(node1) != len(node2):
            return f'List length mismatch at {path}: {len(node1)} != {len(node2)}'
        for index, (elem1, elem2) in enumerate(zip(node1, node2)):
            result = ast_equal(elem1, elem2, path=f'{path}[{index}]')
            if result:
                errors.append(result)
    else:
        if node1 != node2:
            return f'Value mismatch at {path}: {node1} != {node2}'

    if errors:
        return '\n'.join(errors)
    return ''


def test_ast_equal_with_identical_literals():
    node1 = ast.Literal(value=42)
    node2 = ast.Literal(value=42)
    assert ast_equal(node1, node2) == '', "Identical literals should have no differences"


def test_ast_equal_with_different_literals():
    node1 = ast.Literal(value=42)
    node2 = ast.Literal(value=43)
    result = ast_equal(node1, node2)
    assert result != '', "Different literals should be reported"


def test_ast_equal_with_different_types():
    node1 = ast.Literal(value=42)
    node2 = ast.UnaryOp(op='-', operand=ast.Literal(value=42))
    result = ast_equal(node1, node2)
    assert result != '', "Nodes of different types should be reported"


def test_ast_equal_with_complex_structure():
    node1 = ast.BinaryOp(left=ast.Literal(value=42), op='+', right=ast.Literal(value=1))
    node2 = ast.BinaryOp(left=ast.Literal(value=42), op='+', right=ast.Literal(value=2))
    result = ast_equal(node1, node2)
    assert result != '', "Differences in complex structures should be reported"


def test_ast_equal_with_list_differences():
    node1 = [ast.Literal(value=42), ast.Literal(value=2)]
    node2 = [ast.Literal(value=42)]
    result = ast_equal(node1, node2)
    assert result != '', "Differences in list lengths should be reported"


def test_ast_equal_with_nested_differences():
    node1 = ast.BinaryOp(left=ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.Literal(value=2)), op='*',
                         right=ast.Literal(value=3))
    node2 = ast.BinaryOp(left=ast.BinaryOp(left=ast.Literal(value=1), op='-', right=ast.Literal(value=2)), op='*',
                         right=ast.Literal(value=3))
    result = ast_equal(node1, node2)
    assert result != '', "Nested differences should be reported"
