# /mnt/g/ai/projects/neurocore/tools/system/process_top.py

from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class ProcessTop(BaseTool):

    name = "process_top"
    description = "Retrieve top CPU and memory consuming processes"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        return

    def execute(self, request: Dict[str, Dict]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)

        trace_event(
            event="process_top_collection_started",
            context=ctx,
            component="process_top"
        )

        cpu_result = CommandRunner.run(["ps", "aux", "--sort=-%cpu"])
        mem_result = CommandRunner.run(["ps", "aux", "--sort=-%mem"])

        cpu_parsed = self._parse_ps_output(cpu_result.get("stdout", ""))
        mem_parsed = self._parse_ps_output(mem_result.get("stdout", ""))

        data = {
            "cpu_top": cpu_parsed[:5],
            "memory_top": mem_parsed[:5],
            "raw": {
                "cpu": cpu_result,
                "memory": mem_result
            }
        }

        message = "Top Processes (CPU & Memory)"

        trace_event(
            event="process_top_execution_completed",
            context=ctx,
            component="process_top",
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

    def _parse_ps_output(self, output: str) -> List[Dict[str, Any]]:
        lines = output.splitlines()

        if not lines:
            return []

        header = lines[0]
        rows = lines[1:]

        parsed = []

        for row in rows:
            parts = row.split(None, 10)

            if len(parts) < 11:
                continue

            try:
                parsed.append({
                    "user": parts[0],
                    "pid": int(parts[1]),
                    "cpu_percent": float(parts[2]),
                    "mem_percent": float(parts[3]),
                    "vsz": int(parts[4]),
                    "rss": int(parts[5]),
                    "tty": parts[6],
                    "stat": parts[7],
                    "start": parts[8],
                    "time": parts[9],
                    "command": parts[10]
                })
            except Exception:
                continue

        return parsed