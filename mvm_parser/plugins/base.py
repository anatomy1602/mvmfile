from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..data_object import DataObject


class ComponentPlugin(ABC):
    name: str = ""

    @abstractmethod
    def render(self, section: "DataObject", children: list) -> str:
        ...

    def get_css(self) -> str:
        return ""

    def get_js(self) -> str:
        return ""
