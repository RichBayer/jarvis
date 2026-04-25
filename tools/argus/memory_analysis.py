from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class MemoryAnalysis(BaseTool):

    name = "memory_analysis"
    description = "Analyze system memory usage"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_memory_analysis_invoked",
            context=ctx,
            component="memory_analysis"
        )

        system_tool = registry.get("memory_usage")

        if not system_tool:
            raise ToolValidationError("memory_usage tool not available")

        system_request = {
            "tool": "memory_usage",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve memory data",
                data={}
            )

        data = result.get("data", {})
        mem = data.get("memory", {})

        # -------------------------
        # PARSE MEMORY VALUES
        # -------------------------

        def parse_gib(value: str) -> float:
            try:
                if value.endswith("Gi"):
                    return float(value.replace("Gi", ""))
                if value.endswith("Mi"):
                    return float(value.replace("Mi", "")) / 1024
                if value.endswith("B"):
                    return 0.0
            except Exception:
                return 0.0
            return 0.0

        total = parse_gib(mem.get("total", "0Gi"))
        used = parse_gib(mem.get("used", "0Gi"))

        usage = (used / total * 100) if total > 0 else 0

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        # -------------------------
        # INTERPRETATION LOGIC
        # -------------------------

        if usage > 90:
            severity = "CRITICAL"
        elif usage > 75:
            severity = "WARN"
        elif usage > 50:
            severity = "INFO"
        else:
            severity = "OK"

        findings.append({
            "severity": severity,
            "component": "memory",
            "message": f"Memory usage at {usage:.1f}%",
            "evidence": mem
        })

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------

        if severity in ["WARN", "CRITICAL"]:
            recommendations.append("Investigate memory usage and running processes")

        message = f"Memory Analysis [{severity}]"

        trace_event(
            event="argus_memory_analysis_completed",
            context=ctx,
            component="memory_analysis",
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