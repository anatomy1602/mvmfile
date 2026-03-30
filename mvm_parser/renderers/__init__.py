"""
View 渲染器基类
"""

from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, result) -> str:
        pass

    @abstractmethod
    def file_extension(self) -> str:
        pass
