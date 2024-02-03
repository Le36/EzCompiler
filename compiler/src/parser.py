import compiler.src.ast as ast

from compiler.src.tokenizer import Token

operators_precedence = [
    ['='],
    ['or'],
    ['and'],
    ['==', '!='],
    ['<', '<=', '>', '>='],
    ['+', '-'],
    ['*', '/', '%'],
]

unary_operators = ['not', '-']


class ParseException(Exception):
    pass


def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0

    def peek() -> Token:
        if pos >= len(tokens):
            return Token(location=tokens[-1].location, type="end", text="")
        return tokens[pos]

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        if pos >= len(tokens):
            raise ParseException(f'Unexpected end of input: expected {expected}')
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise ParseException(f'{token.location}: expected "{expected}", got "{token.text}"')
        elif isinstance(expected, list) and token.text not in expected:
            expected_str = ", ".join([f'"{e}"' for e in expected])
            raise ParseException(f'{token.location}: expected one of: {expected_str}, got "{token.text}"')
        pos += 1
        return token

    def parse_int_literal() -> ast.Literal:
        token = consume()
        return ast.Literal(value=int(token.text))

    def parse_boolean_literal() -> ast.Literal:
        token = consume()
        value = True if token.text == 'true' else False
        return ast.Literal(value=value)

    def parse_identifier() -> ast.Identifier:
        token = consume()
        return ast.Identifier(name=token.text)

    def parse_parenthesized() -> ast.Expression:
        consume('(')
        expr = parse_expression()
        consume(')')
        return expr

    def parse_factor() -> ast.Expression:
        if peek().type == 'PUNCTUATION':
            if peek().text == '(':
                return parse_parenthesized()
            elif peek().text == '{':
                return parse_block()
        elif peek().type == 'INTEGER':
            return parse_int_literal()
        elif peek().type == 'BOOLEAN':
            return parse_boolean_literal()
        elif peek().type == 'IDENTIFIER':
            identifier = parse_identifier()
            if peek().text == '(':
                return parse_function_call(identifier)
            else:
                return identifier
        elif peek().type == 'KEYWORD':
            if peek().text == 'if':
                return parse_if_expression()
            elif peek().text == 'while':
                return parse_while()
        else:
            raise ParseException(f'{peek().location}: unexpected token "{peek().text}"')

    def parse_block() -> ast.Block:
        consume('{')
        expressions = []
        result_expression = None
        while peek().text != '}':
            if peek().type == 'KEYWORD' and peek().text == 'var':
                expr = parse_var_declaration()
            else:
                expr = parse_expression()

            if peek().text == ';':
                consume(';')
                expressions.append(expr)
            elif peek().text == '}':
                result_expression = expr
            else:
                raise ParseException(f"Expected ';' or '}}', found {peek().text}")

        consume('}')

        if result_expression is None and expressions:
            result_expression = ast.Literal(value=None)

        return ast.Block(expressions=expressions, result_expression=result_expression)

    def parse_while() -> ast.While:
        consume('while')
        condition = parse_expression()
        consume('do')
        body = parse_expression()
        return ast.While(condition=condition, body=body)

    def parse_var_declaration() -> ast.VarDeclaration:
        consume('var')
        if peek().type != 'IDENTIFIER':
            raise ParseException(f"Expected variable name after 'var', found {peek().text}")
        name = parse_identifier()
        consume('=')
        value = parse_expression()
        return ast.VarDeclaration(name=name.name, value=value)

    def parse_function_call(identifier: ast.Identifier) -> ast.FunctionCall:
        consume('(')
        arguments = []
        if peek().text != ')':
            while True:
                arguments.append(parse_expression())
                if peek().text == ')':
                    break
                consume(',')
        consume(')')
        return ast.FunctionCall(name=identifier.name, arguments=arguments)

    def parse_if_expression() -> ast.IfExpression:
        consume('if')
        condition = parse_expression()
        consume('then')
        then_branch = parse_expression()
        else_branch = None
        if peek().text == 'else':
            consume('else')
            else_branch = parse_expression()
        return ast.IfExpression(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def parse_expression(precedence=0) -> ast.Expression:
        if precedence == len(operators_precedence):
            return parse_unary_expression()

        left_expr = parse_expression(precedence + 1)

        while peek().text in operators_precedence[precedence]:
            op_token = consume()
            right_expr = parse_expression(precedence if op_token.text == '=' else precedence + 1)
            left_expr = ast.BinaryOp(left=left_expr, op=op_token.text, right=right_expr)

        return left_expr

    def parse_unary_expression() -> ast.Expression:
        if peek().text in unary_operators:
            operator_token = consume()
            operand = parse_unary_expression()
            return ast.UnaryOp(op=operator_token.text, operand=operand)
        return parse_factor()

    if not tokens:
        raise ParseException('Empty input provided')

    result = parse_expression()

    if pos < len(tokens):
        raise ParseException(f'Unexpected tokens at end of input: {tokens[pos].text}')

    return result
