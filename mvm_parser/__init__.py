"""
MVM File Parser - .mvm 文件格式解析器
解析 MODEL 和 MSG 区，输出结构化数据
"""

from .blocker import Blocker
from .model_parser import ModelParser
from .msg_parser import MsgParser
from .schema import Schema, TypeDefinition, FieldDefinition, FieldType
from .data_object import DataObject
from .parser import MVMParser

__version__ = "0.1.0"

__all__ = [
    "Blocker",
    "ModelParser",
    "MsgParser",
    "MVMParser",
    "Schema",
    "TypeDefinition",
    "FieldDefinition",
    "FieldType",
    "DataObject",
]
