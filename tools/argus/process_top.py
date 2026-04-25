from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class ProcessTopAnalysis(BaseTool):

    name = "process_top_analysis"
    description = "Analyze top CPU and memory consuming processes"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_process_top_invoked",
            context=ctx,
            component="process_top_analysis"
        )

        system_tool = registry.get("process_top")

        if not system_tool:
            raise ToolValidationError("process_top system tool not available")

        system_request = {
            "tool": "process_top",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve process data",
                data={}
            )

        data = result.get("data", {})

        cpu_top = data.get("cpu_top", [])
        mem_top = data.get("memory_top", [])

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        # High CPU usage detection
        for proc in cpu_top:
            if proc.get("cpu_percent", 0) > 80:
                findings.append({
                    "severity": "WARN",
                    "component": "cpu",
                    "message": f"High CPU usage detected: {proc.get('command')}",
                    "evidence": proc
                })

        # High memory usage detection
        for proc in mem_top:
            if proc.get("mem_percent", 0) > 50:
                findings.append({
                    "severity": "WARN",
                    "component": "memory",
                    "message": f"High memory usage detected: {proc.get('command')}",
                    "evidence": proc
                })

        if not findings:
            findings.append({
                "severity": "OK",
                "component": "processes",
                "message": "No abnormal CPU or memory usage detected",
                "evidence": {}
            })

        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]
        highest_severity = "OK"

        for f in findings:
            if severity_priority.index(f["severity"]) > severity_priority.index(highest_severity):
                highest_severity = f["severity"]

        if highest_severity in ["WARN", "CRITICAL"]:
            recommendations.append("Investigate high resource usage processes")

        message = f"Process Analysis [{highest_severity}]"

        trace_event(
            event="argus_process_top_completed",
            context=ctx,
            component="process_top_analysis",
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