from __future__ import annotations

from typing import Dict, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class MemoryUsage(BaseTool):

    name = "memory_usage"
    description = "Retrieve system memory usage"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        return

    def execute(self, request: Dict[str, Dict]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="memory_usage_collection_started",
            context=ctx,
            component="memory_usage"
        )

        result = CommandRunner.run(["free", "-h"])
        parsed = self._parse_free_output(result.get("stdout", ""))

        data = {
            "memory": parsed.get("memory", {}),
            "swap": parsed.get("swap", {}),
            "raw": result
        }

        message = "Memory usage collected"

        trace_event(
            event="memory_usage_execution_completed",
            context=ctx,
            component="memory_usage",
            status="success"
        )

        return self.build_result(
            status="success",
            message=message,
            data=data
        )

    # -------------------------
    # PARSER
    # -------------------------

    def _parse_free_output(self, output: str) -> Dict[str, Any]:
        lines = output.splitlines()

        if len(lines) < 2:
            return {}

        headers = lines[0].split()
        memory_values = lines[1].split()
        swap_values = lines[2].split() if len(lines) > 2 else []

        memory = {}
        swap = {}

        try:
            if memory_values[0].lower().startswith("mem"):
                memory = {
                    "total": memory_values[1],
                    "used": memory_values[2],
                    "free": memory_values[3],
                    "shared": memory_values[4],
                    "buff_cache": memory_values[5],
                    "available": memory_values[6],
                }

            if swap_values and swap_values[0].lower().startswith("swap"):
                swap = {
                    "total": swap_values[1],
                    "used": swap_values[2],
                    "free": swap_values[3],
                }

        except Exception:
            return {}

        return {
            "memory": memory,
            "swap": swap
        }