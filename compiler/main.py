import sys

from compiler.src.assembler import assemble
from compiler.src.assembly_generator import generate_assembly
from compiler.src.ir_generator import generate_ir, IrException
from compiler.src.parser import parse, ParseException
from compiler.src.sym_table import SymTable
from compiler.src.tokenizer import tokenize
from compiler.src.type import Int, Bool, Unit, FunType, initialize_root_types
from compiler.src.type_checker import typecheck


def read_source_code(input_file):
    """
    Reads the source code from a file or stdin if no file is provided.
    """
    if input_file is not None:
        with open(input_file, 'r') as file:
            return file.read()
    else:
        return sys.stdin.read()


def interpret(source_code, file_name):
    try:
        tokens = tokenize(source_code)
        ast = parse(tokens)
        global_symtable = SymTable()
        typecheck(ast, global_symtable)
        root_types = initialize_root_types()
        ir_instructions = generate_ir(root_types, ast)
        asm = generate_assembly(ir_instructions)
        file_generated = False
        try:
            print(assemble(asm, 'a.out'))
            file_generated = True
        except Exception as e:
            pass
        return {'ast': ast, 'tokens': tokens, 'ir': ir_instructions, 'asm': asm, 'file_generated': file_generated}
    except ParseException as e:
        return {'error': str(e)}
    except TypeError as e:
        return {'error': str(e)}
    except IrException as e:
        return {'error': str(e)}


def process_command(command, input_file=None, source_code=None):
    """
    Processes the given command with either an input file or source code.
    """
    if command == 'interpret':
        file_name = input_file if input_file else 'editor'
        code_to_process = read_source_code(input_file) if input_file else source_code
        return interpret(code_to_process, file_name)
    else:
        print(f"Error: unknown command: {command}")
        return 1


def main():
    usage = "Usage: main.py [command] [input_file]\nCommands:\n- interpret"

    # Parsing command line arguments
    command = None
    input_file = None

    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:
            print(usage)
            return 0
        elif arg.startswith('-'):
            raise Exception(f"Unknown argument: {arg}")
        elif command is None:
            command = arg
        elif input_file is None:
            input_file = arg
        else:
            raise Exception("Multiple input files not supported")

    if command is None:
        print("Error: command argument missing\n\n" + usage, file=sys.stderr)
        return 1

    return process_command(command, input_file)


if __name__ == '__main__':
    sys.exit(main())
