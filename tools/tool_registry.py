# /mnt/g/ai/projects/neurocore/tools/tool_registry.py

from __future__ import annotations

from typing import Dict, List

from tools.base_tool import BaseTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")

        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> List[str]:
        return sorted(self._tools.keys())

    def clear(self) -> None:
        self._tools.clear()


registry = ToolRegistry()