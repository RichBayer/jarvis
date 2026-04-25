# /mnt/g/ai/projects/neurocore/tools/base_tool.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class ToolValidationError(Exception):
    pass


class ToolExecutionError(Exception):
    pass


class BaseTool(ABC):
    name: str = ""
    description: str = ""
    input_schema: Dict[str, Any] = {}
    execution_mode: str = "manual"

    def __init__(self) -> None:
        self._validate_definition()

    def _validate_definition(self) -> None:
        if not self.name:
            raise ValueError("Tool must define a name")

        if not self.description:
            raise ValueError("Tool must define a description")

        if not isinstance(self.input_schema, dict):
            raise ValueError("input_schema must be a dict")

        if self.execution_mode not in {"dry-run", "manual", "auto"}:
            raise ValueError("Invalid execution_mode")

    def get_definition(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "execution_mode": self.execution_mode,
        }

    def validate_request(self, request: Dict[str, Any]) -> None:
        if "tool" not in request:
            raise ToolValidationError("Missing tool field")

        if request["tool"] != self.name:
            raise ToolValidationError("Tool mismatch")

        if "input" not in request:
            raise ToolValidationError("Missing input field")

        if not isinstance(request["input"], dict):
            raise ToolValidationError("Input must be a dict")

        required = self.input_schema.get("required", [])
        missing = [f for f in required if f not in request["input"]]

        if missing:
            raise ToolValidationError(f"Missing fields: {missing}")

        self.validate_input(request["input"])

    @abstractmethod
    def validate_input(self, tool_input: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def build_result(
        self,
        status: str,
        message: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        ENFORCED CONTRACT:
        - data is REQUIRED
        - message is for humans
        - data is for machines
        """

        if not isinstance(data, dict):
            raise ToolExecutionError("Tool must return structured data dict")

        return {
            "status": status,
            "tool": self.name,
            "message": message,
            "data": data,
        }