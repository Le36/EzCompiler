import pytest
from compiler.src.tokenizer import tokenize
from compiler.src.parser import parse, ParseException
import compiler.src.ast as ast
from compiler.tests.test_ast_utils import ast_equal


def test_parse_single_integer():
    source_code = '42'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.Literal(value=42)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_simple_addition():
    source_code = '1 + 2'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.Literal(value=2))
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_variable_assignment():
    source_code = 'x = 5'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(left=ast.Identifier(name='x'), op='=', right=ast.Literal(value=5))
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_empty_input():
    source_code = ''
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_complex_expression():
    source_code = '3 + 5 * 2 - 4 / 2'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(
        left=ast.BinaryOp(
            left=ast.Literal(value=3),
            op='+',
            right=ast.BinaryOp(left=ast.Literal(value=5), op='*', right=ast.Literal(value=2))
        ),
        op='-',
        right=ast.BinaryOp(left=ast.Literal(value=4), op='/', right=ast.Literal(value=2))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_right_associative_assignment():
    source_code = 'x = y = 5'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(
        left=ast.Identifier(name='x'),
        op='=',
        right=ast.BinaryOp(left=ast.Identifier(name='y'), op='=', right=ast.Literal(value=5))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_parentheses_precedence():
    source_code = '(3 + 5) * 2'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(
        left=ast.BinaryOp(left=ast.Literal(value=3), op='+', right=ast.Literal(value=5)),
        op='*',
        right=ast.Literal(value=2)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


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


def test_parse_unexpected_end_of_input():
    source_code = '3 +'
    tokens = tokenize(source_code, 'test')
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_if_then_else():
    source_code = 'if a then b + c else x * y'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.IfExpression(
        condition=ast.Identifier(name='a'),
        then_branch=ast.BinaryOp(left=ast.Identifier(name='b'), op='+', right=ast.Identifier(name='c')),
        else_branch=ast.BinaryOp(left=ast.Identifier(name='x'), op='*', right=ast.Identifier(name='y'))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_if_then():
    source_code = 'if a then b + c'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.IfExpression(
        condition=ast.Identifier(name='a'),
        then_branch=ast.BinaryOp(left=ast.Identifier(name='b'), op='+', right=ast.Identifier(name='c'))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_if_expression_in_arithmetic():
    source_code = '1 + if true then 2 else 3'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(
        left=ast.Literal(value=1),
        op='+',
        right=ast.IfExpression(
            condition=ast.Literal(value=True),
            then_branch=ast.Literal(value=2),
            else_branch=ast.Literal(value=3)
        )
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_boolean_literal():
    source_code_true = 'true'
    tokens_true = tokenize(source_code_true, 'test')
    result_ast_true = parse(tokens_true)
    expected_ast_true = ast.Literal(value=True)
    comparison_result = ast_equal(result_ast_true, expected_ast_true)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'

    source_code_false = 'false'
    tokens_false = tokenize(source_code_false, 'test')
    result_ast_false = parse(tokens_false)
    expected_ast_false = ast.Literal(value=False)
    comparison_result = ast_equal(result_ast_false, expected_ast_false)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_simple_function_call():
    source_code = 'f(x)'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.FunctionCall(name='f', arguments=[ast.Identifier(name='x')])
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_function_call_with_multiple_arguments():
    source_code = 'sum(x, y, z)'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.FunctionCall(
        name='sum',
        arguments=[ast.Identifier(name='x'), ast.Identifier(name='y'), ast.Identifier(name='z')]
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_nested_function_call():
    source_code = 'f(g(x), h(y, z))'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.FunctionCall(
        name='f',
        arguments=[
            ast.FunctionCall(name='g', arguments=[ast.Identifier(name='x')]),
            ast.FunctionCall(name='h', arguments=[ast.Identifier(name='y'), ast.Identifier(name='z')])
        ]
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_function_call_in_expression():
    source_code = '1 + f(x)'
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    expected_ast = ast.BinaryOp(
        left=ast.Literal(value=1),
        op='+',
        right=ast.FunctionCall(name='f', arguments=[ast.Identifier(name='x')])
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


@pytest.mark.parametrize("source_code,expected_ast", [
    ("1 + 2", ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.Literal(value=2))),
    ("3 * 4", ast.BinaryOp(left=ast.Literal(value=3), op='*', right=ast.Literal(value=4))),
    ("5 - 2", ast.BinaryOp(left=ast.Literal(value=5), op='-', right=ast.Literal(value=2))),
    ("6 / 3", ast.BinaryOp(left=ast.Literal(value=6), op='/', right=ast.Literal(value=3))),
    ("7 % 2", ast.BinaryOp(left=ast.Literal(value=7), op='%', right=ast.Literal(value=2))),
    ("1 + 2 * 3", ast.BinaryOp(left=ast.Literal(value=1), op='+',
                               right=ast.BinaryOp(left=ast.Literal(value=2), op='*', right=ast.Literal(value=3)))),
    ("(1 + 2) * 3",
     ast.BinaryOp(left=ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.Literal(value=2)), op='*',
                  right=ast.Literal(value=3))),
])
def test_arithmetic_operators(source_code, expected_ast):
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


@pytest.mark.parametrize("source_code,expected_ast", [
    ("a == b", ast.BinaryOp(left=ast.Identifier(name='a'), op='==', right=ast.Identifier(name='b'))),
    ("a != b", ast.BinaryOp(left=ast.Identifier(name='a'), op='!=', right=ast.Identifier(name='b'))),
    ("a < b", ast.BinaryOp(left=ast.Identifier(name='a'), op='<', right=ast.Identifier(name='b'))),
    ("a <= b", ast.BinaryOp(left=ast.Identifier(name='a'), op='<=', right=ast.Identifier(name='b'))),
    ("a > b", ast.BinaryOp(left=ast.Identifier(name='a'), op='>', right=ast.Identifier(name='b'))),
    ("a >= b", ast.BinaryOp(left=ast.Identifier(name='a'), op='>=', right=ast.Identifier(name='b'))),
])
def test_comparison_operators(source_code, expected_ast):
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


@pytest.mark.parametrize("source_code,expected_ast", [
    ("true and false", ast.BinaryOp(left=ast.Literal(value=True), op='and', right=ast.Literal(value=False))),
    ("true or false", ast.BinaryOp(left=ast.Literal(value=True), op='or', right=ast.Literal(value=False))),
])
def test_logical_operators(source_code, expected_ast):
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


@pytest.mark.parametrize("source_code,expected_ast", [
    ("not x", ast.UnaryOp(op='not', operand=ast.Identifier(name='x'))),
    ("-x", ast.UnaryOp(op='-', operand=ast.Identifier(name='x'))),
    ("not not x", ast.UnaryOp(op='not', operand=ast.UnaryOp(op='not', operand=ast.Identifier(name='x')))),
])
def test_unary_operators(source_code, expected_ast):
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


@pytest.mark.parametrize("source_code,expected_ast", [
    ("1 + 2 * 3 == 7", ast.BinaryOp(
        ast.BinaryOp(ast.Literal(1), '+', ast.BinaryOp(ast.Literal(2), '*', ast.Literal(3))),
        '==',
        ast.Literal(7)
    )),

    ("a < b and c > d or e == f", ast.BinaryOp(
        ast.BinaryOp(
            ast.BinaryOp(ast.Identifier('a'), '<', ast.Identifier('b')),
            'and',
            ast.BinaryOp(ast.Identifier('c'), '>', ast.Identifier('d'))
        ),
        'or',
        ast.BinaryOp(ast.Identifier('e'), '==', ast.Identifier('f'))
    )),

    ("not x + y", ast.BinaryOp(
        ast.UnaryOp('not', ast.Identifier('x')),
        '+',
        ast.Identifier('y')
    )),

    ("x = y or z", ast.BinaryOp(
        ast.Identifier('x'),
        '=',
        ast.BinaryOp(ast.Identifier('y'), 'or', ast.Identifier('z'))
    )),

    ("1 + f(2, 3) * 4", ast.BinaryOp(
        ast.Literal(1),
        '+',
        ast.BinaryOp(
            ast.FunctionCall('f', [ast.Literal(2), ast.Literal(3)]),
            '*',
            ast.Literal(4)
        )
    )),

    ("not not true == false", ast.BinaryOp(
        ast.UnaryOp('not', ast.UnaryOp('not', ast.Literal(True))),
        '==',
        ast.Literal(False)
    )),

    ("1 + if a then b else c", ast.BinaryOp(
        ast.Literal(1),
        '+',
        ast.IfExpression(ast.Identifier('a'), ast.Identifier('b'), ast.Identifier('c'))
    )),
])
def test_operator_precedence(source_code, expected_ast):
    tokens = tokenize(source_code, 'test')
    result_ast = parse(tokens)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'
