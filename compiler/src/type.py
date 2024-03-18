from dataclasses import dataclass
from typing import List, Dict

from compiler.src.ir import IRVar


@dataclass
class Type:
    pass


@dataclass
class Int(Type):
    pass


@dataclass
class Bool(Type):
    pass


@dataclass
class Unit(Type):
    pass


@dataclass
class FunType(Type):
    arg_types: List[Type]
    return_type: Type


INT = Int()
BOOL = Bool()
UNIT = Unit()


def initialize_root_types() -> Dict[IRVar, Type]:
    unary_minus_type = FunType(arg_types=[INT], return_type=INT)
    unary_not_type = FunType(arg_types=[BOOL], return_type=BOOL)
    add_type = FunType(arg_types=[INT, INT], return_type=INT)
    sub_type = FunType(arg_types=[INT, INT], return_type=INT)
    mult_type = FunType(arg_types=[INT, INT], return_type=INT)
    div_type = FunType(arg_types=[INT, INT], return_type=INT)
    mod_type = FunType(arg_types=[INT, INT], return_type=INT)
    lt_type = FunType(arg_types=[INT, INT], return_type=BOOL)
    gt_type = FunType(arg_types=[INT, INT], return_type=BOOL)
    lte_type = FunType(arg_types=[INT, INT], return_type=BOOL)
    gte_type = FunType(arg_types=[INT, INT], return_type=BOOL)
    and_type = FunType(arg_types=[BOOL, BOOL], return_type=BOOL)
    or_type = FunType(arg_types=[BOOL, BOOL], return_type=BOOL)
    print_int_type = FunType(arg_types=[INT], return_type=UNIT)
    print_bool_type = FunType(arg_types=[BOOL], return_type=UNIT)
    read_int_type = FunType(arg_types=[], return_type=INT)

    root_types = {
        IRVar("unary_-"): unary_minus_type,
        IRVar("unary_not"): unary_not_type,
        IRVar("+"): add_type,
        IRVar("-"): sub_type,
        IRVar("*"): mult_type,
        IRVar("/"): div_type,
        IRVar("%"): mod_type,
        IRVar("<"): lt_type,
        IRVar(">"): gt_type,
        IRVar("<="): lte_type,
        IRVar(">="): gte_type,
        IRVar("and"): and_type,
        IRVar("or"): or_type,
        IRVar("print_int"): print_int_type,
        IRVar("print_bool"): print_bool_type,
        IRVar("read_int"): read_int_type,
    }

    return root_types
