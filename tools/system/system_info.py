# /mnt/g/ai/projects/neurocore/tools/system/system_info.py

from __future__ import annotations

from typing import Dict, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.system.command_runner import CommandRunner


class SystemInfo(BaseTool):

    name = "system_info"
    description = "Retrieve read-only system information (cpu, memory, disk, os, uptime)"
    execution_mode = "auto"

    input_schema = {
        "required": ["target"]
    }

    VALID_TARGETS = {
        "system",
        "cpu",
        "memory",
        "disk",
        "os",
        "uptime",
        "hostname",
    }

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        target = tool_input.get("target")

        if target not in self.VALID_TARGETS:
            raise ToolValidationError(
                f"Invalid target '{target}'. Valid targets: {self.VALID_TARGETS}"
            )

    def execute(self, request: Dict[str, Dict]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)
        tool_input = request["input"]

        trace_event(
            event="tool_invoked",
            context=ctx,
            component="system_info",
            details={"input": tool_input}
        )

        target = tool_input["target"]

        trace_event(
            event="system_info_target_selected",
            context=ctx,
            component="system_info",
            details={"target": target}
        )

        if target == "system":
            raw_data = self._system_summary()
        elif target == "cpu":
            raw_data = self._cpu_info()
        elif target == "memory":
            raw_data = self._memory_info()
        elif target == "disk":
            raw_data = self._disk_info()
        elif target == "os":
            raw_data = self._os_info()
        elif target == "uptime":
            raw_data = self._uptime()
        elif target == "hostname":
            raw_data = self._hostname()
        else:
            raise ToolValidationError(f"Unsupported target: {target}")

        trace_event(
            event="system_info_execution_completed",
            context=ctx,
            component="system_info",
            status="success"
        )

        return {
            "status": "success",
            "tool": self.name,
            "message": self._format_output(target, raw_data),
            "data": raw_data  # 🔥 NEW: structured data
        }

    # -------------------------
    # FORMAT OUTPUT (UNCHANGED)
    # -------------------------

    def _format_output(self, target: str, data: Dict[str, Any]) -> str:
        lines = [f"{target.capitalize()} Information\n"]

        for key, value in data.items():
            lines.append(f"{key.capitalize()}:\n{value}\n")

        return "\n".join(lines).strip()

    # -------------------------
    # DATA COLLECTION METHODS
    # -------------------------

    def _hostname(self):
        r = CommandRunner.run(["hostname"])
        return {
            "hostname": r["stdout"]
        }

    def _uptime(self):
        r = CommandRunner.run(["uptime"])
        return {
            "raw": r["stdout"]
        }

    def _os_info(self):
        r = CommandRunner.run(["cat", "/etc/os-release"])
        return {
            "raw": r["stdout"]
        }

    def _cpu_info(self):
        r = CommandRunner.run(["lscpu"])
        return {
            "raw": r["stdout"]
        }

    def _memory_info(self):
        r = CommandRunner.run(["free", "-m"])
        return {
            "raw": r["stdout"]
        }

    def _disk_info(self):
        r = CommandRunner.run(["df", "-h", "/"])
        return {
            "raw": r["stdout"]
        }

    def _system_summary(self):
        return {
            "hostname": self._hostname(),
            "uptime": self._uptime(),
            "os": self._os_info(),
            "cpu": self._cpu_info(),
            "memory": self._memory_info(),
            "disk": self._disk_info(),
        }