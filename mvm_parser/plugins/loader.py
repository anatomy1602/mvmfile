import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type

from .base import ComponentPlugin


class PluginLoader:
    def __init__(self):
        self._plugins: Dict[str, ComponentPlugin] = {}

    def register(self, plugin: ComponentPlugin) -> None:
        name = plugin.name
        if not name:
            raise ValueError("Plugin must have a non-empty name")
        self._plugins[name] = plugin

    def get(self, name: str) -> Optional[ComponentPlugin]:
        return self._plugins.get(name)

    def has(self, name: str) -> bool:
        return name in self._plugins

    def list_names(self) -> List[str]:
        return list(self._plugins.keys())

    def load_from_directory(self, directory: str) -> int:
        plugin_dir = Path(directory)
        if not plugin_dir.is_dir():
            return 0

        loaded = 0
        for py_file in sorted(plugin_dir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue
            try:
                count = self._load_plugin_file(str(py_file))
                loaded += count
            except Exception as e:
                print(f"Warning: Failed to load plugin {py_file}: {e}")
        return loaded

    def _load_plugin_file(self, filepath: str) -> int:
        module_name = f"_mvm_plugin_{Path(filepath).stem}"
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None or spec.loader is None:
            return 0

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        loaded = 0
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, ComponentPlugin)
                and attr is not ComponentPlugin
                and hasattr(attr, "name")
                and attr.name
            ):
                self.register(attr())
                loaded += 1
        return loaded

    def load_builtin_plugins(self) -> None:
        builtin_dir = Path(__file__).parent / "builtin"
        if builtin_dir.is_dir():
            self.load_from_directory(str(builtin_dir))
