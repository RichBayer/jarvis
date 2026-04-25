# /mnt/g/ai/projects/neurocore/tools/system/uptime_load.py

from __future__ import annotations
from typing import Dict, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class UptimeLoad(BaseTool):

    name = "uptime_load"
    description = "Retrieve system uptime and load"
    execution_mode = "auto"

    input_schema = {"required": []}

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="uptime_load_collection_started",
            context=ctx,
            component="uptime_load"
        )

        result = CommandRunner.run(["uptime"])
        parsed = self._parse_uptime_output(result.get("stdout", ""))

        data = {
            **parsed,
            "raw": result
        }

        trace_event(
            event="uptime_load_execution_completed",
            context=ctx,
            component="uptime_load",
            status="success"
        )

        return self.build_result(
            status="success",
            message="Uptime and load collected",
            data=data
        )

    # -------------------------
    # PARSER
    # -------------------------

    def _parse_uptime_output(self, output: str) -> Dict[str, Any]:
        result = {
            "uptime": None,
            "users": None,
            "load_average": {
                "1m": None,
                "5m": None,
                "15m": None
            }
        }

        if not output:
            return result

        try:
            # Example:
            # 16:53:12 up 2 days,  3:41,  1 user,  load average: 0.12, 0.08, 0.05

            parts = output.split(" up ", 1)
            if len(parts) < 2:
                return result

            rest = parts[1]

            # Split before "load average"
            before_load, _, load_part = rest.partition("load average:")

            # Uptime + users section
            segments = before_load.split(",")

            # Extract uptime (first segment)
            result["uptime"] = segments[0].strip()

            # Extract users (find segment with "user")
            for seg in segments:
                if "user" in seg:
                    try:
                        result["users"] = int(seg.strip().split()[0])
                    except Exception:
                        pass

            # Extract load averages
            loads = load_part.strip().split(",")

            if len(loads) >= 3:
                result["load_average"]["1m"] = loads[0].strip()
                result["load_average"]["5m"] = loads[1].strip()
                result["load_average"]["15m"] = loads[2].strip()

        except Exception:
            pass

        return result