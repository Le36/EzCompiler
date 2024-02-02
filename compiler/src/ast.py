from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""


@dataclass
class Literal(Expression):
    value: int | bool | None
    # (value=None is used when parsing the keyword `unit`)


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class BinaryOp(Expression):
    """AST node for a binary operation like `A + B`"""
    left: Expression
    op: str
    right: Expression


@dataclass
class IfExpression(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Expression = None  # `else_branch` is optional


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
