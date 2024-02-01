import pytest
from compiler.src.tokenizer import tokenize
from compiler.src.parser import parse, ParseException
import compiler.src.ast as ast


def test_parse_single_integer():
    source_code = '42'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.Literal(value=42)
    assert isinstance(result_ast, ast.Literal) and result_ast.value == expected_ast.value


def test_parse_simple_addition():
    source_code = '1 + 2'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.BinaryOp)
    assert isinstance(result_ast.left, ast.Literal) and result_ast.left.value == 1
    assert result_ast.op == '+'
    assert isinstance(result_ast.right, ast.Literal) and result_ast.right.value == 2


def test_parse_variable_assignment():
    source_code = 'x = 5'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.BinaryOp)
    assert isinstance(result_ast.left, ast.Identifier) and result_ast.left.name == 'x'
    assert result_ast.op == '='
    assert isinstance(result_ast.right, ast.Literal) and result_ast.right.value == 5


def test_parse_empty_input():
    source_code = ''
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_complex_expression():
    source_code = '3 + 5 * 2 - 4 / 2'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.BinaryOp) and result_ast.op == '-'
    assert isinstance(result_ast.left, ast.BinaryOp) and result_ast.left.op == '+'
    assert isinstance(result_ast.right, ast.BinaryOp) and result_ast.right.op == '/'


def test_parse_right_associative_assignment():
    source_code = 'x = y = 5'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.BinaryOp) and result_ast.op == '='
    assert isinstance(result_ast.right, ast.BinaryOp) and result_ast.right.op == '='
    assert result_ast.right.left.name == 'y'
    assert result_ast.right.right.value == 5


def test_parse_parentheses_precedence():
    source_code = '(3 + 5) * 2'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.BinaryOp) and result_ast.op == '*'
    assert isinstance(result_ast.left, ast.BinaryOp) and result_ast.left.op == '+'


def test_parse_unexpected_token_error():
    source_code = '3 + * 5'
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_missing_operator():
    source_code = '3 5'
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_unsupported_nested_assignments():
    source_code = 'x = (y = 5)'
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_unexpected_end_of_input():
    source_code = '3 +'
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_if_then_else():
    source_code = 'if a then b + c else x * y'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.IfExpression)
    assert isinstance(result_ast.condition, ast.Identifier)
    assert isinstance(result_ast.then_branch, ast.BinaryOp)
    assert isinstance(result_ast.else_branch, ast.BinaryOp)


def test_parse_if_then():
    source_code = 'if a then b + c'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.IfExpression)
    assert result_ast.else_branch is None


def test_parse_if_expression_in_arithmetic():
    source_code = '1 + if true then 2 else 3'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    assert isinstance(result_ast, ast.BinaryOp)
    assert isinstance(result_ast.right, ast.IfExpression)


def test_parse_boolean_literal():
    source_code_true = 'true'
    source_code_false = 'false'
    tokens_true = tokenize(source_code_true, 'test')
    tokens_false = tokenize(source_code_false, 'test')
    result_ast_true = parse(tokens_true)
    result_ast_false = parse(tokens_false)
    assert isinstance(result_ast_true, ast.Literal) and result_ast_true.value is True
    assert isinstance(result_ast_false, ast.Literal) and result_ast_false.value is False
