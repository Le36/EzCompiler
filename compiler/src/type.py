from dataclasses import dataclass
from typing import List


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
