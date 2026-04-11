# /mnt/g/ai/projects/neurocore/tools/execution_engine.py

from __future__ import annotations

from typing import Any, Dict

from tools.base_tool import ToolValidationError, ToolExecutionError
from tools.tool_registry import registry


class ExecutionEngine:
    def __init__(self) -> None:
        self.registry = registry

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if "tool" not in request:
                raise ToolValidationError("Missing tool field")

            if "input" not in request:
                raise ToolValidationError("Missing input field")

            tool_name = request["tool"]

            tool = self.registry.get(tool_name)

            if not tool:
                return {
                    "status": "error",
                    "error_type": "tool_not_found",
                    "message": f"Tool '{tool_name}' not found",
                }

            tool.validate_request(request)

            result = tool.execute(request["input"])

            if not isinstance(result, dict):
                raise ToolExecutionError("Invalid result format")

            return result

        except ToolValidationError as e:
            return {
                "status": "error",
                "error_type": "validation_error",
                "message": str(e),
            }

        except ToolExecutionError as e:
            return {
                "status": "error",
                "error_type": "execution_error",
                "message": str(e),
            }

        except Exception as e:
            return {
                "status": "error",
                "error_type": "internal_error",
                "message": str(e),
            }