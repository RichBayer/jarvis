from __future__ import annotations

from typing import Dict, List, Any

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool, ToolValidationError
from tools.tool_registry import registry


class NetworkAnalysis(BaseTool):

    name = "network_analysis"
    description = "Analyze network interface state"
    execution_mode = "auto"

    input_schema = {
        "required": []
    }

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="argus_network_analysis_invoked",
            context=ctx,
            component="network_analysis"
        )

        system_tool = registry.get("network_interfaces")

        if not system_tool:
            raise ToolValidationError("network_interfaces tool not available")

        system_request = {
            "tool": "network_interfaces",
            "input": {},
            "trace": request.get("trace"),
        }

        result = system_tool.execute(system_request)

        if result.get("status") != "success":
            return self.build_result(
                status="error",
                message="Failed to retrieve network data",
                data={}
            )

        data = result.get("data", {})
        interfaces = data.get("interfaces", [])

        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        severity_priority = ["OK", "INFO", "WARN", "CRITICAL"]
        highest_severity = "OK"

        # -------------------------
        # INTERPRETATION LOGIC
        # -------------------------

        if not interfaces:
            findings.append({
                "severity": "CRITICAL",
                "component": "network",
                "message": "No network interfaces detected",
                "evidence": {}
            })
            highest_severity = "CRITICAL"
        else:
            down_interfaces = []

            for iface in interfaces:
                state = iface.get("state", "").lower()

                if state != "up":
                    down_interfaces.append(iface)

            if down_interfaces:
                findings.append({
                    "severity": "WARN",
                    "component": "network",
                    "message": f"{len(down_interfaces)} interface(s) not up",
                    "evidence": down_interfaces
                })
                highest_severity = "WARN"
            else:
                findings.append({
                    "severity": "OK",
                    "component": "network",
                    "message": "All interfaces are up",
                    "evidence": interfaces
                })

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------

        if highest_severity in ["WARN", "CRITICAL"]:
            recommendations.append("Investigate network interface state and connectivity")

        message = f"Network Analysis [{highest_severity}]"

        trace_event(
            event="argus_network_analysis_completed",
            context=ctx,
            component="network_analysis",
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