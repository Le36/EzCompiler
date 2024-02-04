import pytest

from compiler.src.ast import make_literal, make_binary_op, make_identifier, make_function_call, make_if_expression, \
    make_while, make_block, \
    make_var_declaration, make_unary_op
from compiler.src.parser import parse, ParseException
from compiler.src.tokenizer import tokenize
from compiler.tests.test_ast_utils import ast_equal


def test_parse_single_integer():
    source_code = '42'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_literal(42)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_simple_addition():
    source_code = '1 + 2'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(make_literal(1), '+', make_literal(2))
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_variable_assignment():
    source_code = 'x = 5'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(make_identifier('x'), '=', make_literal(5))
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_empty_input():
    source_code = ''
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_complex_expression():
    source_code = '3 + 5 * 2 - 4 / 2'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(
        make_binary_op(
            make_literal(3),
            '+',
            make_binary_op(make_literal(5), '*', make_literal(2))
        ),
        '-',
        make_binary_op(make_literal(4), '/', make_literal(2))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_right_associative_assignment():
    source_code = 'x = y = 5'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(
        left=make_identifier('x'),
        op='=',
        right=make_binary_op(
            left=make_identifier('y'),
            op='=',
            right=make_literal(5)
        )
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_parentheses_precedence():
    source_code = '(3 + 5) * 2'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(
        left=make_binary_op(
            left=make_literal(3),
            op='+',
            right=make_literal(5)
        ),
        op='*',
        right=make_literal(2)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_unexpected_token_error():
    source_code = '3 + * 5'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_missing_operator():
    source_code = '3 5'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_unexpected_end_of_input():
    source_code = '3 +'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_if_then_else():
    source_code = 'if a then b + c else x * y'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_if_expression(
        condition=make_identifier('a'),
        then_branch=make_binary_op(left=make_identifier('b'), op='+', right=make_identifier('c')),
        else_branch=make_binary_op(left=make_identifier('x'), op='*', right=make_identifier('y'))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_if_then():
    source_code = 'if a then b + c'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_if_expression(
        condition=make_identifier('a'),
        then_branch=make_binary_op(left=make_identifier('b'), op='+', right=make_identifier('c'))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_if_expression_in_arithmetic():
    source_code = '1 + if true then 2 else 3'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(
        left=make_literal(1),
        op='+',
        right=make_if_expression(
            condition=make_literal(True),
            then_branch=make_literal(2),
            else_branch=make_literal(3)
        )
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_boolean_literal():
    source_code_true = 'true'
    tokens_true = tokenize(source_code_true)
    result_ast_true = parse(tokens_true)
    expected_ast_true = make_literal(True)
    comparison_result = ast_equal(result_ast_true, expected_ast_true)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'

    source_code_false = 'false'
    tokens_false = tokenize(source_code_false)
    result_ast_false = parse(tokens_false)
    expected_ast_false = make_literal(False)
    comparison_result = ast_equal(result_ast_false, expected_ast_false)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_simple_function_call():
    source_code = 'f(x)'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_function_call('f', [make_identifier('x')])
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_function_call_with_multiple_arguments():
    source_code = 'sum(x, y, z)'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_function_call(
        'sum',
        [make_identifier('x'), make_identifier('y'), make_identifier('z')]
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_nested_function_call():
    source_code = 'f(g(x), h(y, z))'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_function_call(
        'f',
        [
            make_function_call('g', [make_identifier('x')]),
            make_function_call('h', [make_identifier('y'), make_identifier('z')])
        ]
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_function_call_in_expression():
    source_code = '1 + f(x)'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(
        make_literal(1),
        '+',
        make_function_call('f', [make_identifier('x')])
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_simple_while_loop():
    source_code = 'while x < 5 do x = x + 1'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_while(
        make_binary_op(make_identifier('x'), '<', make_literal(5)),
        make_binary_op(make_identifier('x'), '=', make_binary_op(make_identifier('x'), '+', make_literal(1)))
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_while_loop_missing_do_error():
    source_code = 'while x < 5 x = x + 1'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_simple_block():
    source_code = '{ var x = 10; y = x + 1; 30 }'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_var_declaration('x', make_literal(10)),
            make_binary_op(
                make_identifier('y'), '=',
                make_binary_op(make_identifier('x'), '+', make_literal(1))
            )
        ],
        result_expression=make_literal(30)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_consecutive_expressions_error():
    source_code = '{ a b }'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_complex_block():
    source_code = """
    {
        while f() do {
            x = 10;
            y = if g(x) then {
                x = x + 1;
                x
            } else {
                g(x)
            };
            g(y);
        };
        123
    }
    """
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_while(
                make_function_call('f', []),
                make_block(
                    expressions=[
                        make_binary_op(make_identifier('x'), '=', make_literal(10)),
                        make_binary_op(
                            make_identifier('y'), '=',
                            make_if_expression(
                                make_function_call('g', [make_identifier('x')]),
                                make_block(
                                    expressions=[make_binary_op(make_identifier('x'), '=',
                                                                make_binary_op(make_identifier('x'), '+',
                                                                               make_literal(1)))],
                                    result_expression=make_identifier('x')
                                ),
                                make_block(
                                    expressions=[],
                                    result_expression=make_function_call('g', [make_identifier('x')])
                                )
                            )
                        ),
                        make_function_call('g', [make_identifier('y')])
                    ],
                    result_expression=make_literal(None)
                )
            )
        ],
        result_expression=make_literal(123)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_block_with_final_semicolon():
    source_code = '{ var x = 10; x = x + 1; }'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_var_declaration('x', make_literal(10)),
            make_binary_op(make_identifier('x'), '=', make_binary_op(make_identifier('x'), '+', make_literal(1)))
        ],
        result_expression=make_literal(None)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_block_without_final_semicolon():
    source_code = "{ f(a); x = y; f(x) }"
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_function_call('f', [make_identifier('a')]),
            make_binary_op(make_identifier('x'), '=', make_identifier('y'))
        ],
        result_expression=make_function_call('f', [make_identifier('x')])
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_nested_blocks():
    source_code = """
    {
        if (a) then {
            f(b);
        };
        {
            g(c);
            h(d);
        };
    }
    """
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_if_expression(
                make_identifier('a'),
                make_block(expressions=[make_function_call('f', [make_identifier('b')])],
                           result_expression=make_literal(None))
            ),
            make_block(
                expressions=[
                    make_function_call('g', [make_identifier('c')]),
                    make_function_call('h', [make_identifier('d')])
                ],
                result_expression=make_literal(None)
            )
        ],
        result_expression=make_literal(None)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_empty_block():
    source_code = '{}'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(expressions=[], result_expression=None)
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_block_missing_closing_brace_error():
    source_code = '{ var x = 123;'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_variable_declaration_outside_block_error():
    source_code = 'var x = 123'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException):
        parse(tokens)


def test_parse_nested_no_semicolon():
    source_code = '{ { a } { b } }'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_block(
                expressions=[],
                result_expression=make_identifier('a')
            ),
            make_block(
                expressions=[],
                result_expression=make_identifier('b')
            )
        ],
        result_expression=make_literal(None)
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_conditional_with_block():
    source_code = '{ if true then { a }; b }'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_if_expression(
                condition=make_literal(True),
                then_branch=make_block(
                    expressions=[],
                    result_expression=make_identifier('a')
                )
            )
        ],
        result_expression=make_identifier('b')
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_if_with_nested_blocks_no_semicolon():
    source_code = '{ if true then { a } b }'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_block(
        expressions=[
            make_if_expression(
                condition=make_literal(True),
                then_branch=make_block(
                    expressions=[],
                    result_expression=make_identifier('a')
                )
            )
        ],
        result_expression=make_identifier('b')
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_parse_assignment_with_nested_blocks():
    source_code = 'x = { { f(a) } { b } }'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_binary_op(
        left=make_identifier('x'),
        op='=',
        right=make_block(
            expressions=[
                make_block(
                    expressions=[],
                    result_expression=make_function_call(
                        name='f',
                        arguments=[make_identifier('a')]
                    )
                ),
                make_block(
                    expressions=[],
                    result_expression=make_identifier('b')
                )
            ],
            result_expression=make_literal(None)
        )
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_function_call_argument_error():
    source_code = 'f(a b)'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException) as exc_info:
        parse(tokens)
    assert "Expected a ',' between function arguments or a ')' to close the function call" in str(exc_info.value)


def test_unary_expression_parsing():
    source_code = 'not not x'
    tokens = tokenize(source_code)
    result_ast = parse(tokens)
    expected_ast = make_unary_op(
        op='not',
        operand=make_unary_op(
            op='not',
            operand=make_identifier('x')
        )
    )
    comparison_result = ast_equal(result_ast, expected_ast)
    assert comparison_result == '', f'ASTs do not match:\n{comparison_result}'


def test_var_declaration_error():
    source_code = '{var = 123}'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException) as exc_info:
        parse(tokens)
    assert "Expected variable name after 'var'" in str(exc_info.value)


def test_var_declaration_outside_block():
    source_code = 'var x = 123'
    tokens = tokenize(source_code)
    with pytest.raises(ParseException) as exc_info:
        parse(tokens)
    assert "'var' declarations are only allowed inside blocks" in str(exc_info.value)
