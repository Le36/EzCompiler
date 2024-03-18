import dataclasses

from compiler.src import ir
from compiler.src.intrinsics import all_intrinsics, IntrinsicArgs
from compiler.src.ir import IRVar


class Locals:
    _var_to_location: dict[IRVar, str]
    _stack_used: int

    def __init__(self, variables: list[IRVar]) -> None:
        self._var_to_location = {}
        self._stack_used = 0
        offset = 8

        for var in variables:
            self._stack_used += 8
            self._var_to_location[var] = f"-{offset}(%rbp)"
            offset += 8

    def get_ref(self, v: IRVar) -> str:
        return self._var_to_location[v]

    def stack_used(self) -> int:
        return self._stack_used


def get_all_ir_variables(instructions: list[ir.Instruction]) -> list[ir.IRVar]:
    result_list: list[ir.IRVar] = []
    result_set: set[ir.IRVar] = set()

    def add(v: ir.IRVar) -> None:
        if v not in result_set:
            result_list.append(v)
            result_set.add(v)

    for insn in instructions:
        for field in dataclasses.fields(insn):
            value = getattr(insn, field.name)
            if isinstance(value, ir.IRVar):
                add(value)
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, ir.IRVar):
                        add(v)
    return result_list


def generate_assembly(instructions: list[ir.Instruction]) -> str:
    lines = []

    def emit(line: str) -> None:
        lines.append(line)

    locals = Locals(
        variables=get_all_ir_variables(instructions)
    )

    emit(".extern print_int")
    emit(".extern print_bool")
    emit(".extern read_int")
    emit(".global main")
    emit(".type main, @function")
    emit(".section .text")
    emit("main:")
    emit("    pushq %rbp")
    emit("    movq %rsp, %rbp")
    emit(f"    subq ${locals.stack_used()}, %rsp")

    for insn in instructions:
        emit('# ' + str(insn))
        match insn:
            case ir.Label():
                emit(f'.L{insn.name}:')
            case ir.LoadIntConst():
                if -2 ** 31 <= insn.value < 2 ** 31:
                    emit(f'movq ${insn.value}, {locals.get_ref(insn.dest)}')
                else:
                    emit(f'movabsq ${insn.value}, %rax')
                    emit(f'movq %rax, {locals.get_ref(insn.dest)}')
            case ir.LoadBoolConst():
                value = 1 if insn.value else 0
                emit(f'movq ${value}, {locals.get_ref(insn.dest)}')
            case ir.Copy():
                emit(f'movq {locals.get_ref(insn.source)}, %rax')
                emit(f'movq %rax, {locals.get_ref(insn.dest)}')
            case ir.CondJump():
                emit(f'cmpq $0, {locals.get_ref(insn.cond)}')
                emit(f'jne .L{insn.then_label.name}')
                emit(f'jmp .L{insn.else_label.name}')
            case ir.Jump():
                emit(f'jmp .L{insn.label.name}')
            case ir.Call():
                args = insn.args if isinstance(insn.args, list) else [insn.args]

                if insn.fun.name in all_intrinsics:
                    intrinsic = all_intrinsics[insn.fun.name]
                    arg_refs = [locals.get_ref(arg) for arg in args]
                    intrinsic(IntrinsicArgs(
                        arg_refs=arg_refs,
                        result_register="%rax",
                        emit=emit
                    ))
                    if insn.dest:
                        emit(f'movq %rax, {locals.get_ref(insn.dest)}')
                else:
                    arg_registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
                    for arg, reg in zip(args, arg_registers):
                        emit(f'movq {locals.get_ref(arg)}, {reg}')

                    emit(f'call {insn.fun.name}')

                    if insn.dest:
                        emit(f'movq %rax, {locals.get_ref(insn.dest)}')

    emit("    movq %rbp, %rsp")
    emit("    popq %rbp")
    emit("    ret")

    return "\n".join(lines)
