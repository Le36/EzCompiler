from compiler.src.ast import Expression, Literal, Identifier, BinaryOp, IfExpression, FunctionCall, UnaryOp, Block, \
    While, VarDeclaration
from compiler.src.sym_table import SymTable
from compiler.src.type import Type, INT, BOOL, UNIT, Int, Bool


def typecheck(node: Expression, symtable: SymTable) -> Type:
    match node:
        case Literal(value=value):
            if isinstance(value, bool):
                node.type = BOOL
                return BOOL
            elif isinstance(value, int):
                node.type = INT
                return INT
            elif value is None:
                return UNIT
            else:
                raise TypeError(f"Unsupported literal type: {type(value)}. Location: {node.location}")

        case Identifier(name=name):
            try:
                node.type = symtable.lookup(name)
                return node.type
            except LookupError:
                raise TypeError(f"Undefined variable: '{name}'. Location: {node.location}")

        case BinaryOp(left=left, op=op, right=right):
            if op == '=':
                if not isinstance(left, Identifier):
                    raise TypeError(
                        f"Assignment target must be a variable name. Found type: {type(left).__name__}. "
                        f"Location: {node.location}")
                right_type = typecheck(right, symtable)
                node.type = right_type
                return right_type
            else:
                t1 = typecheck(left, symtable)
                t2 = typecheck(right, symtable)
                if op in ['+', '-', '*', '/', '%']:
                    if not isinstance(t1, Int) or not isinstance(t2, Int):
                        expected_type = 'Int'
                        found_type1 = 'Bool' if isinstance(t1, Bool) else 'Int'
                        found_type2 = 'Bool' if isinstance(t2, Bool) else 'Int'
                        raise TypeError(
                            f"Expected both operands to be {expected_type} for operation '{op}', found {found_type1} "
                            f"and {found_type2}. Location: {node.location}")
                    node.type = INT
                    return INT
                elif op in ['and', 'or']:
                    if isinstance(t1, Bool) and isinstance(t2, Bool):
                        node.type = BOOL
                        return BOOL
                    else:
                        raise TypeError(
                            f"Logical '{op}' operations require Bool type operands. Location: {node.location}")
                elif op in ['==', '!=', '<', '<=', '>', '>=']:
                    if isinstance(t1, Int) and isinstance(t2, Int):
                        node.type = BOOL
                        return BOOL
                    else:
                        raise TypeError(
                            f"Binary comparison operations require Int type operands. Location: {node.location}")
                else:
                    raise TypeError(f"Unsupported binary operator: {op}. Location: {node.location}")

        case UnaryOp(op=op, operand=operand):
            operand_type = typecheck(operand, symtable)
            if op == 'not' and isinstance(operand_type, Bool):
                node.type = BOOL
                return BOOL
            elif op == '-' and isinstance(operand_type, Int):
                node.type = INT
                return INT
            else:
                raise TypeError(
                    f"Unsupported unary operator: {op} for type {type(operand_type).__name__}. "
                    f"Location: {node.location}")

        case IfExpression(condition=condition, then_branch=then_branch, else_branch=else_branch):
            t1 = typecheck(condition, symtable)
            if not isinstance(t1, Bool):
                raise TypeError(f"If condition must be of type Bool Location: {node.location}")
            t2 = typecheck(then_branch, symtable)
            t3 = typecheck(else_branch, symtable) if else_branch else UNIT
            if type(t2) != type(t3):
                raise TypeError(f"The types of then and else branches must match. Location: {node.location}")
            node.type = t2
            return t2

        case FunctionCall(name=name, arguments=arguments):
            allowed_functions = {
                'print_bool': (BOOL,),
                'print_int': (INT,),
                'read_int': ()
            }

            if name not in allowed_functions:
                raise TypeError(f"Undefined function: '{name}'. Location: {node.location}")

            expected_arg_types = allowed_functions[name]

            if len(arguments) != len(expected_arg_types):
                raise TypeError(
                    f"Function '{name}' expects {len(expected_arg_types)} arguments, got {len(arguments)}. "
                    f"Location: {node.location}")

            for arg, expected_type in zip(arguments, expected_arg_types):
                arg_type = typecheck(arg, symtable)
                if type(arg_type) != type(expected_type):
                    raise TypeError(
                        f"Function '{name}' expects arguments of type {expected_type.__class__.__name__}, "
                        f"got {arg_type.__class__.__name__}. Location: {node.location}")

            if name == 'read_int':
                node.type = INT
                return INT
            return UNIT

        case UnaryOp(op=op, operand=operand):
            t = typecheck(operand, symtable)
            if op == '-' and isinstance(t, Int):
                node.type = INT
                return INT
            elif op == '!' and isinstance(t, Bool):
                node.type = BOOL
                return BOOL
            else:
                raise TypeError(
                    f"Unsupported unary operator: {op} for type {type(t).__name__}. Location: {node.location}")

        case Block(expressions=expressions, result_expression=result_expression):
            local_symtable = symtable.new_child()
            for expr in expressions:
                typecheck(expr, local_symtable)
            if result_expression:
                result_type = typecheck(result_expression, local_symtable)
                node.type = result_type
                return result_type
            return UNIT

        case While(condition=condition, body=body):
            t1 = typecheck(condition, symtable)
            if not isinstance(t1, Bool):
                raise TypeError(f"While condition must be of type Bool. Location: {node.location}")
            typecheck(body, symtable)
            return UNIT

        case VarDeclaration(name=name, value=value):
            t = typecheck(value, symtable)
            symtable.define(name, t)
            return UNIT

        case _:
            raise TypeError(f"Unsupported AST node type: {type(node).__name__}. Location: {node.location}")
