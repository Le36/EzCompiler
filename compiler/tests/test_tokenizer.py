from compiler.src.tokenizer import tokenize, Token, L


def test_tokenize_single_identifier():
    assert tokenize('variable') == [Token(text='variable', type='IDENTIFIER', location=L)]


def test_tokenize_mixed_tokens():
    assert tokenize('if x == 123') == [
        Token(text='if', type='KEYWORD', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text='==', type='OPERATOR', location=L),
        Token(text='123', type='INTEGER', location=L)
    ]


def test_tokenize_with_operators():
    assert tokenize('x + y - 3 * 4 / 5') == [
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text='+', type='OPERATOR', location=L),
        Token(text='y', type='IDENTIFIER', location=L),
        Token(text='-', type='OPERATOR', location=L),
        Token(text='3', type='INTEGER', location=L),
        Token(text='*', type='OPERATOR', location=L),
        Token(text='4', type='INTEGER', location=L),
        Token(text='/', type='OPERATOR', location=L),
        Token(text='5', type='INTEGER', location=L)
    ]


def test_tokenize_with_punctuation():
    assert tokenize('foo, bar; baz() {}') == [
        Token(text='foo', type='IDENTIFIER', location=L),
        Token(text=',', type='PUNCTUATION', location=L),
        Token(text='bar', type='IDENTIFIER', location=L),
        Token(text=';', type='PUNCTUATION', location=L),
        Token(text='baz', type='IDENTIFIER', location=L),
        Token(text='(', type='PUNCTUATION', location=L),
        Token(text=')', type='PUNCTUATION', location=L),
        Token(text='{', type='PUNCTUATION', location=L),
        Token(text='}', type='PUNCTUATION', location=L)
    ]


def test_tokenize_ignoring_whitespace_and_comments():
    assert tokenize('   \n var // comment\n 42 # another comment\n') == [
        Token(text='var', type='KEYWORD', location=L),
        Token(text='42', type='INTEGER', location=L)
    ]


def test_tokenize_with_multiline_comments():
    assert tokenize('/* comment \n multiline */ var 123') == [
        Token(text='var', type='KEYWORD', location=L),
        Token(text='123', type='INTEGER', location=L)
    ]


def test_tokenize_empty_string():
    assert tokenize('') == []


def test_tokenize_whitespace_only():
    assert tokenize('   \t\n  ') == []


def test_tokenize_complex_expression():
    assert tokenize('func(a, b + c * 2);') == [
        Token(text='func', type='IDENTIFIER', location=L),
        Token(text='(', type='PUNCTUATION', location=L),
        Token(text='a', type='IDENTIFIER', location=L),
        Token(text=',', type='PUNCTUATION', location=L),
        Token(text='b', type='IDENTIFIER', location=L),
        Token(text='+', type='OPERATOR', location=L),
        Token(text='c', type='IDENTIFIER', location=L),
        Token(text='*', type='OPERATOR', location=L),
        Token(text='2', type='INTEGER', location=L),
        Token(text=')', type='PUNCTUATION', location=L),
        Token(text=';', type='PUNCTUATION', location=L)
    ]


def test_tokenize_exact_location():
    tokens = tokenize('var x = 42\n/* comment \nwelcome*/\n end')

    expected = [
        "Token(text='var', type='KEYWORD', location=SourceLocation(line=1, column=1))",
        "Token(text='x', type='IDENTIFIER', location=SourceLocation(line=1, column=5))",
        "Token(text='=', type='OPERATOR', location=SourceLocation(line=1, column=7))",
        "Token(text='42', type='INTEGER', location=SourceLocation(line=1, column=9))",
        "Token(text='end', type='IDENTIFIER', location=SourceLocation(line=4, column=2))"
    ]

    actual = [str(token) for token in tokens]

    assert actual == expected


def test_tokenize_boolean_literals():
    assert tokenize("true false") == [
        Token(text='true', type='BOOLEAN', location=L),
        Token(text='false', type='BOOLEAN', location=L)
    ]


def test_tokenize_operator_precedence():
    assert tokenize("a + b * c") == [
        Token(text='a', type='IDENTIFIER', location=L),
        Token(text='+', type='OPERATOR', location=L),
        Token(text='b', type='IDENTIFIER', location=L),
        Token(text='*', type='OPERATOR', location=L),
        Token(text='c', type='IDENTIFIER', location=L)
    ]


def test_tokenize_variable_declaration():
    assert tokenize("var x: Int = 10") == [
        Token(text='var', type='KEYWORD', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text=':', type='PUNCTUATION', location=L),
        Token(text='Int', type='KEYWORD', location=L),
        Token(text='=', type='OPERATOR', location=L),
        Token(text='10', type='INTEGER', location=L)
    ]


def test_tokenize_if_then_else_structure():
    assert tokenize("if x then y else z") == [
        Token(text='if', type='KEYWORD', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text='then', type='KEYWORD', location=L),
        Token(text='y', type='IDENTIFIER', location=L),
        Token(text='else', type='KEYWORD', location=L),
        Token(text='z', type='IDENTIFIER', location=L)
    ]


def test_tokenize_while_loop():
    assert tokenize("while x > 1 do { y }") == [
        Token(text='while', type='KEYWORD', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text='>', type='OPERATOR', location=L),
        Token(text='1', type='INTEGER', location=L),
        Token(text='do', type='KEYWORD', location=L),
        Token(text='{', type='PUNCTUATION', location=L),
        Token(text='y', type='IDENTIFIER', location=L),
        Token(text='}', type='PUNCTUATION', location=L)
    ]


def test_tokenize_lib_function_call():
    assert tokenize("print_int(x)") == [
        Token(text='print_int', type='LIBRARY_FUNCTION', location=L),
        Token(text='(', type='PUNCTUATION', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text=')', type='PUNCTUATION', location=L)
    ]


def test_tokenize_assignment_statement():
    assert tokenize("x = 3 * 4") == [
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text='=', type='OPERATOR', location=L),
        Token(text='3', type='INTEGER', location=L),
        Token(text='*', type='OPERATOR', location=L),
        Token(text='4', type='INTEGER', location=L)
    ]


def test_tokenize_block_structure():
    assert tokenize("{ x; y; z }") == [
        Token(text='{', type='PUNCTUATION', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text=';', type='PUNCTUATION', location=L),
        Token(text='y', type='IDENTIFIER', location=L),
        Token(text=';', type='PUNCTUATION', location=L),
        Token(text='z', type='IDENTIFIER', location=L),
        Token(text='}', type='PUNCTUATION', location=L)
    ]


def test_tokenize_unrecognized_symbol():
    assert tokenize("var x: Int = 10 @") == [
        Token(text='var', type='KEYWORD', location=L),
        Token(text='x', type='IDENTIFIER', location=L),
        Token(text=':', type='PUNCTUATION', location=L),
        Token(text='Int', type='KEYWORD', location=L),
        Token(text='=', type='OPERATOR', location=L),
        Token(text='10', type='INTEGER', location=L)
    ]
