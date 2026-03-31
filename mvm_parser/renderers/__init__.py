"""
View 渲染器基类
"""

from abc import ABC, abstractmethod
from typing import ClassVar, List


class BaseRenderer(ABC):
    capabilities: ClassVar[List[str]] = []

    @abstractmethod
    def render(self, result) -> str:
        pass

    @abstractmethod
    def file_extension(self) -> str:
        pass

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    def check_requirements(self, required: List[str]) -> List[str]:
        return [r for r in required if r not in self.capabilities]
