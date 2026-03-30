"""
MVMParser - 顶层解析器
组合 Blocker + ModelParser + MsgParser，提供统一的解析接口
"""

from .blocker import Blocker, BlockerError
from .model_parser import ModelParser, ModelParserError
from .msg_parser import MsgParser, MsgParserError
from .schema import Schema
from .data_object import DataObject


class MVMParseError(Exception):
    pass


class MVMParseResult:
    def __init__(self, schema: Schema, data: DataObject):
        self.schema = schema
        self.data = data

    def to_dict(self) -> dict:
        return {
            "schema": {
                "version": self.schema.version,
                "root_type": self.schema.root_type,
                "types": {
                    name: {
                        "fields": {
                            fname: {
                                "type": str(fdef.type),
                                "required": fdef.required,
                            }
                            for fname, fdef in tdef.fields.items()
                        }
                    }
                    for name, tdef in self.schema.types.items()
                },
            },
            "data": self._data_to_dict(self.data),
        }

    def _data_to_dict(self, obj: DataObject) -> dict:
        result = {"_type": obj.type_name}
        for k, v in obj.fields.items():
            if isinstance(v, DataObject):
                result[k] = self._data_to_dict(v)
            elif isinstance(v, list):
                result[k] = [
                    self._data_to_dict(item) if isinstance(item, DataObject) else item
                    for item in v
                ]
            else:
                result[k] = v
        return result


class MVMParser:
    def __init__(self):
        self.blocker = Blocker()
        self.model_parser = ModelParser()
        self.msg_parser = MsgParser()

    def parse_file(self, filepath: str) -> MVMParseResult:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return self.parse(content)

    def parse(self, content: str) -> MVMParseResult:
        try:
            blocks = self.blocker.parse(content)
        except BlockerError as e:
            raise MVMParseError(f"Block error: {e}") from e

        try:
            schema = self.model_parser.parse(blocks.model_text)
        except ModelParserError as e:
            raise MVMParseError(f"Model error: {e}") from e

        try:
            data = self.msg_parser.parse(blocks.msg_text, schema)
        except MsgParserError as e:
            raise MVMParseError(f"Msg error: {e}") from e

        return MVMParseResult(schema=schema, data=data)
