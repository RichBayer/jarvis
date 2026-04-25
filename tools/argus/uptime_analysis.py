from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class UptimeAnalysis(BaseTool):

    name = "uptime_analysis"
    description = "Analyze system uptime and load averages"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_uptime_analysis_invoked",
            context=ctx,
            component="uptime_analysis"
        )

        system_tool = registry.get("uptime_load")

        if not system_tool:
            raise ToolValidationError("uptime_load tool not available")

        system_request = {
            "tool": "uptime_load",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve uptime data",
                data={}
            )

        data = result.get("data", {})

        load = data.get("load_average", {})
        load_1 = load.get("1min", 0.0)

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        # -------------------------
        # INTERPRETATION LOGIC
        # -------------------------

        if load_1 > 4.0:
            severity = "CRITICAL"
        elif load_1 > 2.0:
            severity = "WARN"
        elif load_1 > 1.0:
            severity = "INFO"
        else:
            severity = "OK"

        findings.append({
            "severity": severity,
            "component": "load",
            "message": f"1-minute load average: {load_1}",
            "evidence": data
        })

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------

        if severity in ["WARN", "CRITICAL"]:
            recommendations.append("Investigate system load and running processes")

        message = f"Uptime Analysis [{severity}]"

        trace_event(
            event="argus_uptime_analysis_completed",
            context=ctx,
            component="uptime_analysis",
            status="success"
        )

        return self.build_result(
            status="success",
            message=message,
            data={
                "severity": severity,
                "findings": findings,
                "recommendations": recommendations
            }
        )