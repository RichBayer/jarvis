# /mnt/g/ai/projects/neurocore/tools/system/service_manager.py

from __future__ import annotations

from typing import Dict

from tools.base_tool import BaseTool, ToolValidationError


class ServiceManager(BaseTool):
    """
    Tool for managing system services (simulated for now).
    """

    name = "service_manager"
    description = "Manage system services (start, stop, restart, status)"
    execution_mode = "manual"

    input_schema = {
        "required": ["action", "service"]
    }

    VALID_ACTIONS = {"start", "stop", "restart", "status"}

    def validate_input(self, tool_input: Dict[str, str]) -> None:
        action = tool_input.get("action")
        service = tool_input.get("service")

        if action not in self.VALID_ACTIONS:
            raise ToolValidationError(
                f"Invalid action '{action}'. Valid actions: {self.VALID_ACTIONS}"
            )

        if not isinstance(service, str) or not service.strip():
            raise ToolValidationError("Service name must be a non-empty string")

    def execute(self, tool_input: Dict[str, str]) -> Dict[str, str]:
        action = tool_input["action"]
        service = tool_input["service"]

        message = f"[SIMULATED] {action} executed on service '{service}'"

        return self.build_result(
            status="success",
            message=message,
            data={
                "action": action,
                "service": service,
                "mode": "simulation"
            }
        )