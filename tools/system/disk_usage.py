# /mnt/g/ai/projects/neurocore/tools/system/disk_usage.py

from __future__ import annotations

from typing import Dict, Any, List

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class DiskUsage(BaseTool):

    name = "disk_usage"
    description = "Retrieve filesystem disk usage"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        return

    def execute(self, request: Dict[str, Dict]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="tool_invoked",
            context=ctx,
            component="disk_usage",
            details={"input": request.get("input", {})}
        )

        trace_event(
            event="disk_usage_collection_started",
            context=ctx,
            component="disk_usage"
        )

        result = CommandRunner.run(["df", "-h"])
        parsed = self._parse_df_output(result.get("stdout", ""))

        data = {
            "filesystems": parsed,
            "raw": result
        }

        message = "Disk usage collected"

        trace_event(
            event="disk_usage_execution_completed",
            context=ctx,
            component="disk_usage",
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

    def _parse_df_output(self, output: str) -> List[Dict[str, Any]]:
        lines = output.splitlines()

        if len(lines) < 2:
            return []

        rows = lines[1:]
        parsed = []

        for row in rows:
            parts = row.split()

            if len(parts) < 6:
                continue

            try:
                parsed.append({
                    "filesystem": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "use_percent": parts[4],
                    "mounted_on": parts[5]
                })
            except Exception:
                continue

        return parsed