import compiler.src.ast as ast

from compiler.src.tokenizer import Token


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

    def parse_identifier() -> ast.Identifier:
        token = consume()
        return ast.Identifier(name=token.text)

    def parse_parenthesized() -> ast.Expression:
        consume('(')
        expr = parse_expression()
        consume(')')
        return expr

    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().type == 'INTEGER':
            return parse_int_literal()
        elif peek().type == 'IDENTIFIER':
            return parse_identifier()
        else:
            raise ParseException(f'{peek().location}: expected "(", an integer literal, or an identifier')

    def parse_term() -> ast.Expression:
        left = parse_factor()
        while peek().text in ['*', '/']:
            operator_token = consume()
            right = parse_factor()
            left = ast.BinaryOp(left=left, op=operator_token.text, right=right)
        return left

    def parse_expression() -> ast.Expression:
        left = parse_term()
        while peek().text in ['+', '-']:
            operator_token = consume()
            right = parse_term()
            left = ast.BinaryOp(left=left, op=operator_token.text, right=right)
        return left

    def parse_assignment() -> ast.Expression:
        expr = parse_expression()
        if peek().text == '=':
            operator_token = consume('=')
            value = parse_assignment()
            expr = ast.BinaryOp(left=expr, op=operator_token.text, right=value)
        return expr

    if not tokens:
        raise ParseException('Empty input provided')

    result = parse_assignment()

    if pos < len(tokens):
        raise ParseException(f'Unexpected tokens at end of input: {tokens[pos].text}')

    return result
