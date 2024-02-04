from dataclasses import dataclass
from typing import List, Optional, Union

from compiler.src.tokenizer import SourceLocation, L


@dataclass
class Expression:
    location: SourceLocation


@dataclass
class Literal(Expression):
    value: Union[int, bool, None]


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class BinaryOp(Expression):
    left: Expression
    op: str
    right: Expression


@dataclass
class IfExpression(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Optional[Expression] = None


@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]


@dataclass
class UnaryOp(Expression):
    op: str
    operand: Expression


@dataclass
class Block(Expression):
    expressions: List[Expression]
    result_expression: Optional[Expression] = None


@dataclass
class While(Expression):
    condition: Expression
    body: Expression


@dataclass
class VarDeclaration(Expression):
    name: str
    value: Expression


def make_expression(location=L) -> Expression:
    return Expression(location=location)


def make_literal(value: Union[int, bool, None], location=L) -> Literal:
    return Literal(value=value, location=location)


def make_identifier(name: str, location=L) -> Identifier:
    return Identifier(name=name, location=location)


def make_binary_op(left: Expression, op: str, right: Expression, location=L) -> BinaryOp:
    return BinaryOp(left=left, op=op, right=right, location=location)


def make_if_expression(condition: Expression, then_branch: Expression, else_branch: Optional[Expression] = None,
                       location=L) -> IfExpression:
    return IfExpression(condition=condition, then_branch=then_branch, else_branch=else_branch, location=location)


def make_function_call(name: str, arguments: List[Expression],
                       location=L) -> FunctionCall:
    return FunctionCall(name=name, arguments=arguments, location=location)


def make_unary_op(op: str, operand: Expression, location=L) -> UnaryOp:
    return UnaryOp(op=op, operand=operand, location=location)


def make_block(expressions: List[Expression], result_expression: Optional[Expression] = None, location=L) -> Block:
    return Block(expressions=expressions, result_expression=result_expression, location=location)


def make_while(condition: Expression, body: Expression, location=L) -> While:
    return While(condition=condition, body=body, location=location)


def make_var_declaration(name: str, value: Expression, location=L) -> VarDeclaration:
    return VarDeclaration(name=name, value=value, location=location)
