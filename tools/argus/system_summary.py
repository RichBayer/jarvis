from __future__ import annotations

from typing import Dict, List

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class SystemSummary(BaseTool):

    name = "system_summary"
    description = "Provide a high-level interpreted system health summary"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_tool_invoked",
            context=ctx,
            component="system_summary"
        )

        system_tool = registry.get("system_info")

        if not system_tool:
            raise ToolValidationError("system_info tool not available")

        system_request = {
            "tool": "system_info",
            "input": {"target": "system"},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve system information",
                data={}
            )

        data = result.get("data", {})

        findings: List[Dict] = []
        recommendations: List[str] = []
        highest_severity = "OK"

        # SIMPLE EXAMPLE — expand later
        findings.append({
            "severity": "OK",
            "message": "System data collected successfully"
        })

        message = f"System Summary [{highest_severity}]"

        trace_event(
            event="argus_summary_completed",
            context=ctx,
            component="system_summary",
            status="success"
        )

        return self.build_result(
            status="success",
            message=message,
            data={
                "severity": highest_severity,
                "findings": findings,
                "recommendations": recommendations
            }
        )