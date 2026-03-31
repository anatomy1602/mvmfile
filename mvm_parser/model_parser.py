"""
ModelParser - 模型解析器
解析 MODEL 区的类型定义，生成 Schema 对象
"""

import re
from .schema import Schema, TypeDefinition, FieldDefinition, FieldType, FieldTypeKind


class ModelParserError(Exception):
    pass


class ModelParser:
    PRIMITIVE_TYPES = {
        "string": FieldTypeKind.STRING,
        "text": FieldTypeKind.TEXT,
        "int": FieldTypeKind.INT,
        "float": FieldTypeKind.FLOAT,
        "bool": FieldTypeKind.BOOL,
        "datetime": FieldTypeKind.DATETIME,
        "url": FieldTypeKind.URL,
    }

    def parse(self, model_text: str) -> Schema:
        schema = Schema()
        lines = model_text.split("\n")
        current_type = None

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            if not stripped or stripped.startswith("//"):
                continue

            if stripped.startswith("@type "):
                type_name = stripped[6:].strip()
                if not type_name:
                    raise ModelParserError(f"Line {line_num}: @type requires a type name")
                current_type = TypeDefinition(name=type_name)
                if not schema.root_type:
                    schema.root_type = type_name
                schema.types[type_name] = current_type
                continue

            if stripped.startswith("@version "):
                schema.version = stripped[9:].strip()
                continue

            if stripped.startswith("@plugins"):
                schema.plugins = self._parse_directive_list(stripped[8:], line_num)
                continue

            if stripped.startswith("@requires"):
                schema.requires = self._parse_directive_list(stripped[9:], line_num)
                continue

            if ":" not in stripped:
                raise ModelParserError(
                    f"Line {line_num}: Expected field definition 'name: type', got '{stripped}'"
                )

            if current_type is None:
                raise ModelParserError(
                    f"Line {line_num}: Field definition found before any @type"
                )

            colon_pos = stripped.index(":")
            field_name = stripped[:colon_pos].strip()
            type_str = stripped[colon_pos + 1:].strip()

            if not field_name:
                raise ModelParserError(f"Line {line_num}: Empty field name")
            if not type_str:
                raise ModelParserError(f"Line {line_num}: Empty type for field '{field_name}'")

            is_optional = type_str.endswith("?")
            if is_optional:
                type_str = type_str[:-1]

            field_type = self._parse_type(type_str, line_num)

            current_type.fields[field_name] = FieldDefinition(
                name=field_name,
                type=field_type,
                required=not is_optional,
            )

        schema.validate()
        return schema

    def _parse_type(self, type_str: str, line_num: int) -> FieldType:
        if type_str in self.PRIMITIVE_TYPES:
            return FieldType(kind=self.PRIMITIVE_TYPES[type_str])

        if type_str.startswith("array<") and type_str.endswith(">"):
            inner = type_str[6:-1].strip()
            if not inner:
                raise ModelParserError(f"Line {line_num}: array<> requires an element type")
            element_type = self._parse_type(inner, line_num)
            return FieldType(kind=FieldTypeKind.ARRAY, element_type=element_type)

        if type_str.startswith("map<") and type_str.endswith(">"):
            inner = type_str[4:-1].strip()
            if "," not in inner:
                raise ModelParserError(
                    f"Line {line_num}: map<> requires key and value types separated by ','"
                )
            parts = inner.split(",", 1)
            key_type = parts[0].strip()
            value_type = parts[1].strip()
            if key_type != "string":
                raise ModelParserError(
                    f"Line {line_num}: map key type must be 'string', got '{key_type}'"
                )
            value_field_type = self._parse_type(value_type, line_num)
            return FieldType(kind=FieldTypeKind.MAP, element_type=value_field_type)

        if type_str.startswith("enum(") and type_str.endswith(")"):
            inner = type_str[5:-1].strip()
            if not inner:
                raise ModelParserError(f"Line {line_num}: enum() requires at least one value")
            values = [v.strip() for v in inner.split("|")]
            if any(not v for v in values):
                raise ModelParserError(f"Line {line_num}: enum values cannot be empty")
            return FieldType(kind=FieldTypeKind.ENUM, enum_values=values)

        if re.match(r"^[A-Z][a-zA-Z0-9]*$", type_str):
            return FieldType(kind=FieldTypeKind.REF, ref_name=type_str)

        raise ModelParserError(f"Line {line_num}: Unknown type '{type_str}'")

    def _parse_directive_list(self, text: str, line_num: int) -> list[str]:
        text = text.strip()
        if not text:
            return []
        if text.startswith("[") and text.endswith("]"):
            inner = text[1:-1].strip()
            if not inner:
                return []
            return [v.strip() for v in inner.split(",") if v.strip()]
        return [v.strip() for v in text.split(",") if v.strip()]
