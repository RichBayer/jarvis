# /mnt/g/ai/projects/neurocore/tools/system/users_sessions.py

from __future__ import annotations
from typing import Dict, Any, List

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class UsersSessions(BaseTool):

    name = "users_sessions"
    description = "Retrieve active user sessions"
    execution_mode = "auto"

    input_schema = {"required": []}

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="users_sessions_collection_started",
            context=ctx,
            component="users_sessions"
        )

        result = CommandRunner.run(["who"])
        parsed = self._parse_who_output(result.get("stdout", ""))

        data = {
            "sessions": parsed,
            "raw": result
        }

        trace_event(
            event="users_sessions_execution_completed",
            context=ctx,
            component="users_sessions",
            status="success"
        )

        return self.build_result(
            status="success",
            message="User sessions collected",
            data=data
        )

    # -------------------------
    # PARSER
    # -------------------------

    def _parse_who_output(self, output: str) -> List[Dict[str, Any]]:
        lines = output.splitlines()
        sessions = []

        for line in lines:
            parts = line.split()

            if len(parts) < 2:
                continue

            try:
                entry = {
                    "user": parts[0],
                    "terminal": parts[1],
                    "login_time": " ".join(parts[2:4]) if len(parts) >= 4 else None,
                    "source": parts[4].strip("()") if len(parts) >= 5 else None
                }

                sessions.append(entry)

            except Exception:
                continue

        return sessions