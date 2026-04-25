from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class DiskAnalysis(BaseTool):

    name = "disk_analysis"
    description = "Analyze system disk usage"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_disk_analysis_invoked",
            context=ctx,
            component="disk_analysis"
        )

        system_tool = registry.get("disk_usage")

        if not system_tool:
            raise ToolValidationError("disk_usage tool not available")

        system_request = {
            "tool": "disk_usage",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve disk data",
                data={}
            )

        data = result.get("data", {})
        filesystems = data.get("filesystems", [])

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        highest_severity = "OK"
        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]

        # -------------------------
        # INTERPRETATION LOGIC
        # -------------------------

        for fs in filesystems:
            use_percent_str = fs.get("use_percent", "0%").replace("%", "")

            try:
                usage = int(use_percent_str)
            except ValueError:
                continue

            if usage > 90:
                severity = "CRITICAL"
            elif usage > 75:
                severity = "WARN"
            elif usage > 50:
                severity = "INFO"
            else:
                continue  # skip low usage

            findings.append({
                "severity": severity,
                "component": "disk",
                "message": f"High disk usage on {fs.get('mounted_on')} ({usage}%)",
                "evidence": fs
            })

            if severity_priority.index(severity) > severity_priority.index(highest_severity):
                highest_severity = severity

        # No issues
        if not findings:
            findings.append({
                "severity": "OK",
                "component": "disk",
                "message": "No abnormal disk usage detected",
                "evidence": {}
            })

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------

        if highest_severity in ["WARN", "CRITICAL"]:
            recommendations.append("Investigate disk usage and free up space")

        message = f"Disk Analysis [{highest_severity}]"

        trace_event(
            event="argus_disk_analysis_completed",
            context=ctx,
            component="disk_analysis",
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