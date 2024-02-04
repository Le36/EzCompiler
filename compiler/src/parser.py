import compiler.src.ast as ast
from compiler.src.ast import Expression, Block

from compiler.src.tokenizer import Token, SourceLocation

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

    def peek(offset: int = 0) -> Token:
        new_pos = pos + offset
        if new_pos < 0 or new_pos >= len(tokens):
            return Token(location=tokens[-1].location, type="end", text="")
        return tokens[new_pos]

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        if pos >= len(tokens):
            expected_str = expected if isinstance(expected, str) \
                else ", ".join(expected) if isinstance(expected, list) else "end of statement"
            raise ParseException(f'Unexpected end of input. Were you missing "{expected_str}"?')
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise ParseException(f'Error at {token.location}: Expected "{expected}", but found "{token.text}".')
        elif isinstance(expected, list) and token.text not in expected:
            expected_str = ", ".join([f'"{e}"' for e in expected])
            raise ParseException(f'Error at {token.location}: Expected one of: {expected_str},'
                                 f' but found "{token.text}". Check for typos or misplaced syntax.')
        pos += 1
        return token

    def parse_int_literal() -> ast.Literal:
        token = consume()
        return ast.Literal(value=int(token.text), location=token.location)

    def parse_boolean_literal() -> ast.Literal:
        token = consume()
        value = True if token.text == 'true' else False
        return ast.Literal(value=value, location=token.location)

    def parse_identifier() -> ast.Identifier:
        token = consume()
        return ast.Identifier(name=token.text, location=token.location)

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
            elif peek().text == 'var':
                raise ParseException(f"Error at {peek().location}: 'var' declarations are only allowed inside blocks.")
        else:
            raise ParseException(
                f'Error at {peek().location}: Unexpected token "{peek().text}". '
                f'Expected an expression (e.g., a literal, identifier, "if", "while", function call, etc.).')

    def parse_block() -> ast.Block:
        open_brace_token = consume('{')
        expressions = []
        result_expression = None
        while peek().text != '}':
            if peek().type == 'KEYWORD' and peek().text == 'var':
                expr = parse_var_declaration()
            else:
                expr = parse_expression()

            if peek().text == ';' or peek(-1).text == '}':
                if peek().text == ';':
                    consume(';')
                expressions.append(expr)
            elif peek().text == '}':
                result_expression = expr
            else:
                raise ParseException(f"Expected ';' or '}}', found {peek().text}")

        consume('}')

        if result_expression is None and expressions:
            result_expression = ast.Literal(value=None, location=open_brace_token.location)

        return ast.Block(expressions=expressions, result_expression=result_expression,
                         location=open_brace_token.location)

    def parse_while() -> ast.While:
        while_token = consume('while')
        condition = parse_expression()
        consume('do')
        body = parse_expression()
        return ast.While(condition=condition, body=body, location=while_token.location)

    def parse_var_declaration() -> ast.VarDeclaration:
        var_token = consume('var')
        if peek().type != 'IDENTIFIER':
            raise ParseException(f"Expected variable name after 'var', found {peek().text}")
        name = parse_identifier()
        consume('=')
        value = parse_expression()
        return ast.VarDeclaration(name=name.name, value=value, location=var_token.location)

    def parse_function_call(identifier: ast.Identifier) -> ast.FunctionCall:
        consume('(')
        arguments = []
        if peek().text != ')':
            while True:
                arguments.append(parse_expression())
                if peek().text == ')':
                    break
                if peek().text != ',':
                    raise ParseException(f"Error at {peek().location}: Expected a ',' between function "
                                         f"arguments or a ')' to close the function call, found '{peek().text}'.")
                consume(',')
        consume(')')
        return ast.FunctionCall(name=identifier.name, arguments=arguments, location=identifier.location)

    def parse_if_expression() -> ast.IfExpression:
        if_token = consume('if')
        condition = parse_expression()
        consume('then')
        then_branch = parse_expression()
        else_branch = None
        if peek().text == 'else':
            consume('else')
            else_branch = parse_expression()
        return ast.IfExpression(condition=condition, then_branch=then_branch, else_branch=else_branch,
                                location=if_token.location)

    def parse_expression(precedence=0) -> ast.Expression:
        if precedence == len(operators_precedence):
            return parse_unary_expression()

        left_expr = parse_expression(precedence + 1)

        while peek().text in operators_precedence[precedence]:
            op_token = consume()
            right_expr = parse_expression(precedence if op_token.text == '=' else precedence + 1)
            left_expr = ast.BinaryOp(left=left_expr, op=op_token.text, right=right_expr, location=op_token.location)

        return left_expr

    def parse_unary_expression() -> ast.Expression:
        if peek().text in unary_operators:
            operator_token = consume()
            operand = parse_unary_expression()
            return ast.UnaryOp(op=operator_token.text, operand=operand, location=operator_token.location)
        return parse_factor()

    def parse_program() -> Expression | Block:
        expressions = []
        while pos < len(tokens):
            expr = parse_expression()
            expressions.append(expr)
            if peek().type == "end" or peek().text != ';':
                break
            consume(';')

        if expressions and peek(-1).text != ";":
            result_expression = expressions.pop()
        else:
            result_expression = ast.Literal(value=None, location=expressions[0].location)

        if not expressions and result_expression:
            return result_expression

        return ast.Block(expressions=expressions, result_expression=result_expression, location=tokens[0].location)

    if not tokens:
        raise ParseException('Empty input provided')

    result = parse_program()

    if pos < len(tokens):
        raise ParseException(f'Unexpected tokens at end of input: {tokens[pos].text}')

    return result
