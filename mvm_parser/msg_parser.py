"""
MsgParser - 内容解析器
按 Schema 验证 MSG 区内容，生成 DataObject
"""

from .schema import Schema, TypeDefinition, FieldDefinition, FieldType, FieldTypeKind
from .data_object import DataObject


class MsgParserError(Exception):
    pass


class MsgParser:
    def parse(self, msg_text: str, schema: Schema) -> DataObject:
        root_type_def = schema.get_type(schema.root_type)
        if root_type_def is None:
            raise MsgParserError(f"Root type '{schema.root_type}' not found in schema")

        lines = msg_text.split("\n")
        data, _ = self._parse_object(lines, 0, root_type_def, schema, indent=0)
        return data

    def _parse_object(
        self,
        lines: list[str],
        start: int,
        type_def: TypeDefinition,
        schema: Schema,
        indent: int = 0,
        data: DataObject | None = None,
    ) -> tuple[DataObject, int]:
        if data is None:
            data = DataObject(type_name=type_def.name)
        i = start

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped or stripped.startswith("//"):
                i += 1
                continue

            current_indent = self._get_indent(line)

            if current_indent < indent:
                break

            if current_indent > indent:
                raise MsgParserError(
                    f"Line {i + 1}: Unexpected indentation increase without field context"
                )

            if stripped.startswith("## "):
                break

            if ":" not in stripped:
                raise MsgParserError(
                    f"Line {i + 1}: Expected 'field: value', got '{stripped}'"
                )

            colon_pos = stripped.index(":")
            field_name = stripped[:colon_pos].strip()
            value_str = stripped[colon_pos + 1:].strip()

            field_def = type_def.fields.get(field_name)
            if field_def is None:
                raise MsgParserError(
                    f"Line {i + 1}: Unknown field '{field_name}' in type '{type_def.name}'"
                )

            i = self._parse_field_value(
                lines, i, data, field_name, field_def, value_str, schema, indent
            )

        for fname, fdef in type_def.fields.items():
            if fdef.required and fname not in data.fields:
                raise MsgParserError(
                    f"Required field '{fname}' is missing in type '{type_def.name}'"
                )

        return data, i

    def _parse_field_value(
        self,
        lines: list[str],
        line_idx: int,
        data: DataObject,
        field_name: str,
        field_def: FieldDefinition,
        value_str: str,
        schema: Schema,
        indent: int,
    ) -> int:
        i = line_idx
        ftype = field_def.type

        if ftype.kind == FieldTypeKind.ARRAY:
            return self._parse_array_field(
                lines, i, data, field_name, field_def, value_str, schema, indent
            )

        if ftype.kind == FieldTypeKind.MAP:
            return self._parse_map_field(
                lines, i, data, field_name, field_def, value_str, schema, indent
            )

        if ftype.kind == FieldTypeKind.TEXT:
            return self._parse_text_field(
                lines, i, data, field_name, value_str, indent
            )

        if ftype.kind == FieldTypeKind.REF:
            if value_str:
                raise MsgParserError(
                    f"Line {i + 1}: Ref field '{field_name}' should not have inline value"
                )
            ref_type_def = schema.get_type(ftype.ref_name)
            if ref_type_def is None:
                raise MsgParserError(
                    f"Line {i + 1}: Referenced type '{ftype.ref_name}' not found"
                )
            obj, i = self._parse_object(lines, i + 1, ref_type_def, schema, indent + 2)
            data.fields[field_name] = obj
            return i

        data.fields[field_name] = self._cast_value(value_str, ftype)
        return i + 1

    def _parse_array_field(
        self,
        lines: list[str],
        line_idx: int,
        data: DataObject,
        field_name: str,
        field_def: FieldDefinition,
        value_str: str,
        schema: Schema,
        indent: int,
    ) -> int:
        i = line_idx
        elem_type = field_def.type.element_type

        if elem_type and elem_type.kind == FieldTypeKind.REF:
            return self._parse_ref_array_field(
                lines, i, data, field_name, elem_type, value_str, schema, indent
            )

        if value_str.startswith("[") and "]" in value_str:
            data.fields[field_name] = self._parse_inline_array(value_str, elem_type, i)
            return i + 1

        if value_str == "":
            items = []
            i += 1
            while i < len(lines):
                item_line = lines[i]
                item_stripped = item_line.strip()
                if not item_stripped:
                    i += 1
                    continue
                item_indent = self._get_indent(item_line)
                if item_indent <= indent:
                    break
                if item_stripped.startswith("- "):
                    item_value = item_stripped[2:].strip()
                    items.append(self._cast_value(item_value, elem_type))
                    i += 1
                else:
                    raise MsgParserError(
                        f"Line {i + 1}: Array items must start with '- ', got '{item_stripped}'"
                    )
            data.fields[field_name] = items
            return i

        raise MsgParserError(
            f"Line {i + 1}: Invalid array value format for field '{field_name}'"
        )

    def _parse_ref_array_field(
        self,
        lines: list[str],
        line_idx: int,
        data: DataObject,
        field_name: str,
        elem_type: FieldType,
        value_str: str,
        schema: Schema,
        indent: int,
    ) -> int:
        i = line_idx

        if value_str:
            raise MsgParserError(
                f"Line {i + 1}: array<{elem_type.ref_name}> must use ## syntax for each item"
            )

        if field_name not in data.fields:
            data.fields[field_name] = []

        i += 1
        while i < len(lines):
            sub_line = lines[i]
            sub_stripped = sub_line.strip()
            if not sub_stripped or sub_stripped.startswith("//"):
                i += 1
                continue
            sub_indent = self._get_indent(sub_line)
            if sub_indent < indent + 2:
                break
            if sub_indent > indent + 2:
                raise MsgParserError(
                    f"Line {i + 1}: Unexpected indentation in array items"
                )
            if not sub_stripped.startswith("## "):
                raise MsgParserError(
                    f"Line {i + 1}: array<RefType> items must start with ##, got '{sub_stripped}'"
                )

            ref_field_str = sub_stripped[3:].strip()
            if ":" not in ref_field_str:
                raise MsgParserError(
                    f"Line {i + 1}: ## item must have 'field: value' format"
                )
            cp = ref_field_str.index(":")
            inline_field = ref_field_str[:cp].strip()
            inline_value = ref_field_str[cp + 1:].strip()

            ref_type_def = schema.get_type(elem_type.ref_name)
            if ref_type_def is None:
                raise MsgParserError(
                    f"Line {i + 1}: Referenced type '{elem_type.ref_name}' not found"
                )

            obj = DataObject(type_name=ref_type_def.name)
            if inline_field and inline_value:
                if inline_field in ref_type_def.fields:
                    fd = ref_type_def.fields[inline_field]
                    obj.fields[inline_field] = self._cast_value(inline_value, fd.type)
            obj, i = self._parse_object(lines, i + 1, ref_type_def, schema, indent + 2, obj)
            data.fields[field_name].append(obj)

        return i

    def _parse_map_field(
        self,
        lines: list[str],
        line_idx: int,
        data: DataObject,
        field_name: str,
        field_def: FieldDefinition,
        value_str: str,
        schema: Schema,
        indent: int,
    ) -> int:
        i = line_idx

        if value_str == "":
            map_data = {}
            i += 1
            while i < len(lines):
                map_line = lines[i]
                map_stripped = map_line.strip()
                if not map_stripped:
                    i += 1
                    continue
                map_indent = self._get_indent(map_line)
                if map_indent <= indent:
                    break
                if ":" in map_stripped:
                    mk, mv = map_stripped.split(":", 1)
                    map_data[mk.strip()] = self._cast_value(
                        mv.strip(), field_def.type.element_type
                    )
                    i += 1
                else:
                    raise MsgParserError(
                        f"Line {i + 1}: Map entries must be 'key: value'"
                    )
            data.fields[field_name] = map_data
            return i

        raise MsgParserError(
            f"Line {i + 1}: Map fields must use multi-line format"
        )

    def _parse_text_field(
        self,
        lines: list[str],
        line_idx: int,
        data: DataObject,
        field_name: str,
        value_str: str,
        indent: int,
    ) -> int:
        i = line_idx

        if value_str == "|":
            text_lines = []
            i += 1
            while i < len(lines):
                text_line = lines[i]
                text_stripped = text_line.strip()
                text_indent = self._get_indent(text_line)
                if text_indent <= indent:
                    break
                if not text_stripped:
                    text_lines.append("")
                    i += 1
                    continue
                text_lines.append(text_stripped)
                i += 1
            data.fields[field_name] = "\n".join(text_lines).strip()
            return i

        data.fields[field_name] = value_str
        return i + 1

    def _parse_inline_array(self, value_str: str, element_type: FieldType, line_num: int) -> list:
        inner = value_str[1 : value_str.index("]")]
        if not inner.strip():
            return []
        items = [item.strip() for item in inner.split(",")]
        return [self._cast_value(item, element_type) for item in items]

    def _cast_value(self, value: str, field_type: FieldType):
        if field_type is None:
            return value

        kind = field_type.kind

        if kind == FieldTypeKind.STRING:
            return value
        elif kind == FieldTypeKind.TEXT:
            return value
        elif kind == FieldTypeKind.INT:
            try:
                return int(value)
            except ValueError:
                raise MsgParserError(f"Cannot convert '{value}' to int")
        elif kind == FieldTypeKind.FLOAT:
            try:
                return float(value)
            except ValueError:
                raise MsgParserError(f"Cannot convert '{value}' to float")
        elif kind == FieldTypeKind.BOOL:
            if value.lower() in ("true", "yes", "1"):
                return True
            elif value.lower() in ("false", "no", "0"):
                return False
            raise MsgParserError(f"Cannot convert '{value}' to bool")
        elif kind == FieldTypeKind.DATETIME:
            return value
        elif kind == FieldTypeKind.URL:
            return value
        elif kind == FieldTypeKind.ENUM:
            if field_type.enum_values and value in field_type.enum_values:
                return value
            raise MsgParserError(
                f"'{value}' is not a valid enum value, expected one of: {field_type.enum_values}"
            )
        elif kind == FieldTypeKind.REF:
            return value

        return value

    def _get_indent(self, line: str) -> int:
        return len(line) - len(line.lstrip())
