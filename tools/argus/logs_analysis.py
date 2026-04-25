from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class LogsAnalysis(BaseTool):

    name = "logs_analysis"
    description = "Analyze system logs for errors and warnings"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_logs_analysis_invoked",
            context=ctx,
            component="logs_analysis"
        )

        system_tool = registry.get("system_logs")

        if not system_tool:
            raise ToolValidationError("system_logs tool not available")

        system_request = {
            "tool": "system_logs",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve logs",
                data={}
            )

        data = result.get("data", {})
        logs = data.get("logs", [])

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]
        highest_severity = "OK"

        # -------------------------
        # INTERPRETATION LOGIC
        # -------------------------

        error_count = 0
        warning_count = 0

        for line in logs:
            line_lower = line.lower()

            if "error" in line_lower:
                error_count += 1
            elif "warn" in line_lower:
                warning_count += 1

        if error_count > 0:
            findings.append({
                "severity": "WARN",
                "component": "logs",
                "message": f"{error_count} error(s) detected in logs",
                "evidence": {"errors": error_count}
            })
            highest_severity = "WARN"
        elif warning_count > 0:
            findings.append({
                "severity": "INFO",
                "component": "logs",
                "message": f"{warning_count} warning(s) detected in logs",
                "evidence": {"warnings": warning_count}
            })
            highest_severity = "INFO"
        else:
            findings.append({
                "severity": "OK",
                "component": "logs",
                "message": "No errors or warnings detected in logs",
                "evidence": {}
            })

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------

        if highest_severity == "WARN":
            recommendations.append("Review system logs for recurring errors")

        message = f"Logs Analysis [{highest_severity}]"

        trace_event(
            event="argus_logs_analysis_completed",
            context=ctx,
            component="logs_analysis",
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