from __future__ import annotations

from typing import Dict

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

    def execute(self, request: Dict[str, Dict]) -> Dict[str, Dict]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="memory_usage_collection_started",
            context=ctx,
            component="memory_usage"
        )

        result = CommandRunner.run(["free", "-h"])
        lines = result["stdout"].splitlines()

        data = {
            "memory_table": lines,
            "raw": lines
        }

        message = "Memory usage collected"

        return self.build_result(
            status="success",
            message=message,
            data=data
        )