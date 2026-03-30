"""
DataObject - 解析后的数据对象
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class DataObject:
    type_name: str
    fields: dict[str, Any] = field(default_factory=dict)

    def get(self, name: str, default: Any = None) -> Any:
        return self.fields.get(name, default)

    def __repr__(self):
        lines = [f"DataObject({self.type_name})"]
        for k, v in self.fields.items():
            if isinstance(v, list):
                lines.append(f"  {k}: [{len(v)} items]")
            elif isinstance(v, DataObject):
                lines.append(f"  {k}: DataObject({v.type_name})")
            else:
                val = str(v)
                if len(val) > 60:
                    val = val[:57] + "..."
                lines.append(f"  {k}: {val}")
        return "\n".join(lines)
