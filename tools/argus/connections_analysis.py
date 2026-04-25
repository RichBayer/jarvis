from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class ConnectionsAnalysis(BaseTool):

    name = "connections_analysis"
    description = "Analyze active network connections"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_connections_analysis_invoked",
            context=ctx,
            component="connections_analysis"
        )

        system_tool = registry.get("network_connections")

        if not system_tool:
            raise ToolValidationError("network_connections tool not available")

        system_request = {
            "tool": "network_connections",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve connection data",
                data={}
            )

        data = result.get("data", {})
        connections = data.get("connections", [])

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]
        highest_severity = "OK"

        # -------------------------
        # INTERPRETATION LOGIC
        # -------------------------

        if not connections:
            findings.append({
                "severity": "INFO",
                "component": "network",
                "message": "No active network connections detected",
                "evidence": {}
            })
            highest_severity = "INFO"
        else:
            high_count_threshold = 200

            if len(connections) > high_count_threshold:
                findings.append({
                    "severity": "WARN",
                    "component": "network",
                    "message": f"High number of active connections ({len(connections)})",
                    "evidence": {"count": len(connections)}
                })
                highest_severity = "WARN"
            else:
                findings.append({
                    "severity": "OK",
                    "component": "network",
                    "message": f"{len(connections)} active connections",
                    "evidence": {"count": len(connections)}
                })

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------

        if highest_severity == "WARN":
            recommendations.append("Investigate unusually high number of connections")

        message = f"Connections Analysis [{highest_severity}]"

        trace_event(
            event="argus_connections_analysis_completed",
            context=ctx,
            component="connections_analysis",
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