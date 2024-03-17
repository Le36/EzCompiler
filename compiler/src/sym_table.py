from typing import Any

from compiler.src.type import Type


class SymTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name: str, type: Type):
        self.symbols[name] = type

    def lookup(self, name: str) -> Type:
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise LookupError(f"Undefined variable: {name}")

    def new_child(self):
        return SymTable(self)

    def update_or_define(self, name: str, type: Type):
        if self.lookup_without_error(name) is not None:
            self.symbols[name] = type
        else:
            self.define(name, type)

    def lookup_without_error(self, name: str) -> Any | None:
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup_without_error(name)
        return None
