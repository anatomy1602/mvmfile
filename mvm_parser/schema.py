"""
Schema 数据结构定义
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class FieldTypeKind(Enum):
    STRING = "string"
    TEXT = "text"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DATETIME = "datetime"
    URL = "url"
    ARRAY = "array"
    MAP = "map"
    ENUM = "enum"
    REF = "ref"


@dataclass
class FieldType:
    kind: FieldTypeKind
    element_type: Optional["FieldType"] = None
    enum_values: Optional[list[str]] = None
    ref_name: Optional[str] = None

    def __repr__(self):
        if self.kind == FieldTypeKind.ARRAY and self.element_type:
            return f"array<{self.element_type}>"
        if self.kind == FieldTypeKind.MAP and self.element_type:
            return f"map<string, {self.element_type}>"
        if self.kind == FieldTypeKind.ENUM and self.enum_values:
            return f"enum({'|'.join(self.enum_values)})"
        if self.kind == FieldTypeKind.REF:
            return f"ref<{self.ref_name}>"
        return self.kind.value


@dataclass
class FieldDefinition:
    name: str
    type: FieldType
    required: bool = True
    default_value: Optional[str] = None


@dataclass
class TypeDefinition:
    name: str
    fields: dict[str, FieldDefinition] = field(default_factory=dict)


@dataclass
class Schema:
    version: str = "1.0"
    root_type: str = ""
    types: dict[str, TypeDefinition] = field(default_factory=dict)

    def get_type(self, name: str) -> Optional[TypeDefinition]:
        return self.types.get(name)

    def validate(self):
        if not self.root_type:
            raise ValueError("Schema must have a root type defined")
        if self.root_type not in self.types:
            raise ValueError(f"Root type '{self.root_type}' is not defined in schema")
