from __future__ import annotations

from typing import Dict, List, Any

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

        raw_data = result.get("data", {})

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        raw_outputs: Dict[str, str] = {}

        def extract_stdout(section: Dict) -> str:
            return section.get("raw", {}).get("stdout", "")

        cpu_output = extract_stdout(raw_data.get("cpu", {}))
        memory_output = extract_stdout(raw_data.get("memory", {}))
        disk_output = extract_stdout(raw_data.get("disk", {}))
        uptime_output = extract_stdout(raw_data.get("uptime", {}))
        os_output = extract_stdout(raw_data.get("os", {}))
        hostname_output = extract_stdout(raw_data.get("hostname", {}))

        raw_outputs["cpu"] = cpu_output
        raw_outputs["memory"] = memory_output
        raw_outputs["disk"] = disk_output
        raw_outputs["uptime"] = uptime_output
        raw_outputs["os"] = os_output
        raw_outputs["hostname"] = hostname_output

        if not cpu_output:
            findings.append({
                "severity": "WARN",
                "component": "cpu",
                "message": "CPU data missing",
                "evidence": raw_data.get("cpu", {})
            })

        if not memory_output:
            findings.append({
                "severity": "WARN",
                "component": "memory",
                "message": "Memory data missing",
                "evidence": raw_data.get("memory", {})
            })

        if not disk_output:
            findings.append({
                "severity": "WARN",
                "component": "disk",
                "message": "Disk data missing",
                "evidence": raw_data.get("disk", {})
            })

        if not uptime_output:
            findings.append({
                "severity": "WARN",
                "component": "uptime",
                "message": "Uptime data missing",
                "evidence": raw_data.get("uptime", {})
            })

        if not os_output:
            findings.append({
                "severity": "WARN",
                "component": "os",
                "message": "OS data missing",
                "evidence": raw_data.get("os", {})
            })

        if not hostname_output:
            findings.append({
                "severity": "WARN",
                "component": "hostname",
                "message": "Hostname data missing",
                "evidence": raw_data.get("hostname", {})
            })

        if not findings:
            findings.append({
                "severity": "OK",
                "component": "system",
                "message": "All system data sources returned successfully",
                "evidence": {}
            })

        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]
        highest_severity = "OK"

        for f in findings:
            if severity_priority.index(f["severity"]) > severity_priority.index(highest_severity):
                highest_severity = f["severity"]

        if highest_severity in ["WARN", "CRITICAL"]:
            recommendations.append("Verify system command outputs and investigate missing data sources")

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
                "recommendations": recommendations,
                "raw": raw_outputs
            }
        )