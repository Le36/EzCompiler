from compiler.src.assembler import assemble
from compiler.src.assembly_generator import generate_assembly
from compiler.src.ir_generator import generate_ir, IrException
from compiler.src.parser import parse, ParseException
from compiler.src.sym_table import SymTable
from compiler.src.tokenizer import tokenize
from compiler.src.type import initialize_root_types
from compiler.src.type_checker import typecheck


def full_compile(source_code):
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
            assemble(asm, 'a.out')
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
