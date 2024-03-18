from typing import Type, Dict, List

from compiler.src.ast import Expression, BinaryOp, Literal, Identifier, IfExpression, Block, VarDeclaration, While, \
    FunctionCall, UnaryOp
from compiler.src.ir import IRVar, LoadBoolConst, LoadIntConst, Call, Instruction, Label, CondJump, Jump, Copy
from compiler.src.sym_table import SymTable
from compiler.src.tokenizer import SourceLocation
from compiler.src.type import Unit, Int, Bool

var_counter = 0
label_counter = {}


def generate_ir(
        root_types: Dict[IRVar, Type],
        root_expr: Expression
) -> List[Instruction]:
    var_types: Dict[IRVar, Type] = root_types.copy()
    var_unit = IRVar('unit')
    var_types[var_unit] = Unit
    ins: List[Instruction] = []

    def new_var(t: Type) -> IRVar:
        global var_counter
        var_counter += 1
        new_var_name = f"x{var_counter}"
        new_var = IRVar(new_var_name)
        var_types[new_var] = t
        return new_var

    def new_label(prefix: str, loc: SourceLocation) -> Label:
        if prefix not in label_counter:
            label_counter[prefix] = 0
        label_counter[prefix] += 1
        label_name = f"{prefix}{label_counter[prefix]}"
        return Label(loc, label_name)

    def visit(st: SymTable, expr: Expression) -> IRVar:
        loc = expr.location

        match expr:
            case Literal():
                match expr.value:
                    case bool():
                        var = new_var(Bool)
                        ins.append(LoadBoolConst(loc, expr.value, var))
                    case int():
                        var = new_var(Int)
                        ins.append(LoadIntConst(loc, expr.value, var))
                    case None:
                        var = var_unit
                    case _:
                        raise Exception(f"{loc}: unsupported literal: {type(expr.value)}")
                return var

            case Identifier():
                return st.lookup(expr.name)

            case BinaryOp():
                if expr.op in ["and", "or"]:
                    l_right = Label(loc, expr.op + '_right')
                    l_skip = Label(loc, expr.op + '_skip')
                    l_end = Label(loc, expr.op + '_end')

                    var_left = visit(st, expr.left)

                    if expr.op == "and":
                        ins.append(CondJump(loc, var_left, l_right, l_skip))
                    elif expr.op == "or":
                        ins.append(CondJump(loc, var_left, l_skip, l_right))

                    ins.append(l_right)

                    var_right = visit(st, expr.right)
                    var_result = new_var(Bool)

                    ins.append(Copy(loc, var_right, var_result))
                    ins.append(Jump(loc, l_end))
                    ins.append(l_skip)

                    ins.append(LoadBoolConst(loc, (expr.op == 'or'), var_result))
                    ins.append(Jump(loc, l_end))
                    ins.append(l_end)

                    return var_result

                if expr.op == "=":
                    if not isinstance(expr.left, Identifier):
                        raise Exception(f"{loc}: Left-hand side of '=' must be an identifier.")

                    var_lhs = st.lookup(expr.left.name)
                    var_rhs = visit(st, expr.right)
                    ins.append(Copy(loc, var_rhs, var_lhs))

                    return var_lhs

                if expr.op == '==' or expr.op == '!=':
                    var_op = IRVar(expr.op)
                else:
                    var_op = st.lookup(expr.op)
                var_left = visit(st, expr.left)
                var_right = visit(st, expr.right)
                var_result = new_var(type(expr))
                ins.append(Call(loc, var_op, [var_left, var_right], var_result))
                return var_result

            case UnaryOp():
                var_op = st.lookup('unary_' + expr.op)
                var_value = visit(st, expr.operand)

                if expr.op == "not":
                    var_result = new_var(Bool)
                elif expr.op == "-":
                    var_result = new_var(Int)
                else:
                    raise Exception(f'{loc}: Unsupported unary operator {expr.op}')

                ins.append(Call(loc, var_op, [var_value], var_result))

                return var_result

            case IfExpression():
                if expr.else_branch is None:
                    l_then = new_label("then", loc)
                    l_end = new_label("if_end", loc)

                    var_cond = visit(st, expr.condition)
                    ins.append(CondJump(loc, var_cond, l_then, l_end))

                    ins.append(l_then)
                    visit(st, expr.then_branch)

                    ins.append(l_end)
                    return var_unit
                else:
                    l_then = new_label("then", loc)
                    l_else = new_label("else", loc)
                    l_end = new_label("if_end", loc)

                    var_cond = visit(st, expr.condition)
                    ins.append(CondJump(loc, var_cond, l_then, l_else))
                    ins.append(l_then)

                    var_result = new_var(expr.then_branch.type)
                    var_then = visit(st, expr.then_branch)
                    ins.append(Copy(loc, var_then, var_result))
                    ins.append(Jump(loc, l_end))
                    ins.append(l_else)
                    var_else = visit(st, expr.else_branch)
                    ins.append(Copy(loc, var_else, var_result))
                    ins.append(l_end)

                    return var_result

            case Block():
                last_var = var_unit

                for expression in expr.expressions:
                    last_var = visit(st, expression)

                if expr.result_expression is not None:
                    last_var = visit(st, expr.result_expression)

                return last_var

            case VarDeclaration():
                var_init_value = visit(st, expr.value)
                var_name = expr.name
                var_ir = new_var(expr.type)

                st.define(var_name, var_ir)
                ins.append(Copy(loc, var_init_value, var_ir))

                return var_ir

            case While():
                l_start = new_label("while_start", loc)
                l_body = new_label("while_body", loc)
                l_end = new_label("while_end", loc)

                ins.append(l_start)
                var_cond = visit(st, expr.condition)
                ins.append(CondJump(loc, var_cond, l_body, l_end))
                ins.append(l_body)

                visit(st, expr.body)

                ins.append(Jump(loc, l_start))
                ins.append(l_end)

                return var_unit

            case FunctionCall():
                if expr.name == "print_int" or expr.name == "print_bool":
                    arg_var = visit(st, expr.arguments[0])
                    var_result = new_var(expr.type)
                    ins.append(Call(loc, st.lookup(expr.name), arg_var, var_result))
                    return var_result
                if expr.name == "read_int":
                    var_result = new_var(expr.type)
                    ins.append(Call(loc, st.lookup(expr.name), [], var_result))
                    return var_result
                else:
                    raise Exception(f"Unsupported function call: {expr.name}")

    root_symtab = SymTable(parent=None)
    global var_counter
    var_counter = 0
    global label_counter
    label_counter = {}
    for var, typ in root_types.items():
        root_symtab.define(var.name, var)

    var_final_result = visit(root_symtab, root_expr)

    if isinstance(root_expr.type, Int):
        ins.append(Call(root_expr.location, IRVar("print_int"), [var_final_result], new_var(Int)))
    elif isinstance(root_expr.type, Bool):
        ins.append(Call(root_expr.location, IRVar("print_bool"), [var_final_result], new_var(Bool)))

    return ins
