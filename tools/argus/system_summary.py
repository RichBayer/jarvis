from __future__ import annotations

from typing import Dict

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
                message="Failed to retrieve system information"
            )

        data = result.get("data", {})

        findings = []
        recommendations = []
        highest_severity = "OK"

        # -------------------------
        # CPU COUNT (for normalization)
        # -------------------------
        cpu_raw = data.get("cpu", {}).get("raw", "")
        cpu_count = 1

        for line in cpu_raw.splitlines():
            if line.lower().startswith("cpu(s):"):
                try:
                    cpu_count = int(line.split(":")[1].strip())
                except Exception:
                    pass

        # -------------------------
        # LOAD ANALYSIS (NORMALIZED)
        # -------------------------
        uptime_raw = data.get("uptime", {}).get("raw", "")

        if "load average" in uptime_raw.lower():
            try:
                load_part = uptime_raw.split("load average:")[1].strip()
                load_value = float(load_part.split(",")[0])
                normalized = load_value / max(cpu_count, 1)

                if normalized > 1.0:
                    findings.append(("CRITICAL", f"Very high system load ({load_value:.2f} total, {normalized:.2f}/core)"))
                    recommendations.append('Investigate CPU-intensive processes (use: ai "processes")')
                    highest_severity = "CRITICAL"
                elif normalized > 0.7:
                    findings.append(("WARNING", f"Elevated system load ({load_value:.2f} total, {normalized:.2f}/core)"))
                    recommendations.append("Monitor system load and identify heavy processes")
                    if highest_severity != "CRITICAL":
                        highest_severity = "WARNING"
                else:
                    findings.append(("OK", f"System load is normal ({load_value:.2f} total, {normalized:.2f}/core)"))

            except Exception:
                pass

        # -------------------------
        # MEMORY ANALYSIS
        # -------------------------
        mem_raw = data.get("memory", {}).get("raw", "")
        lines = mem_raw.splitlines()

        if len(lines) >= 2:
            try:
                parts = lines[1].split()
                total = int(parts[1])
                used = int(parts[2])

                percent = (used / total) * 100

                if percent > 90:
                    findings.append(("CRITICAL", f"Memory usage is critically high ({percent:.1f}%)"))
                    recommendations.append('Check memory-heavy processes (use: ai "processes")')
                    highest_severity = "CRITICAL"
                elif percent > 80:
                    findings.append(("WARNING", f"Memory usage is elevated ({percent:.1f}%)"))
                    recommendations.append("Monitor memory usage and consider freeing resources")
                    if highest_severity != "CRITICAL":
                        highest_severity = "WARNING"
                else:
                    findings.append(("OK", f"Memory usage is normal ({percent:.1f}%)"))

            except Exception:
                pass

        # -------------------------
        # DISK ANALYSIS
        # -------------------------
        disk_raw = data.get("disk", {}).get("raw", "")

        for line in disk_raw.splitlines():
            if "/" in line:
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        usage = int(parts[4].replace("%", ""))

                        if usage > 90:
                            findings.append(("CRITICAL", f"Disk usage is critically high ({usage}%)"))
                            recommendations.append("Free disk space immediately or expand storage")
                            highest_severity = "CRITICAL"
                        elif usage > 80:
                            findings.append(("WARNING", f"Disk usage is high ({usage}%)"))
                            recommendations.append("Clean up unnecessary files or logs")
                            if highest_severity != "CRITICAL":
                                highest_severity = "WARNING"
                        else:
                            findings.append(("OK", f"Disk usage is normal ({usage}%)"))

                    except Exception:
                        pass

        if not findings:
            findings.append(("OK", "System data collected, no issues detected"))

        # -------------------------
        # BUILD OUTPUT
        # -------------------------
        message = f"System Summary [{highest_severity}]\n\n"

        message += "Findings:\n"

        for severity, text in findings:
            prefix = {
                "CRITICAL": "[!!]",
                "WARNING": "[!]",
                "OK": "[OK]"
            }.get(severity, "[ ]")

            message += f"{prefix} {text}\n"

        if recommendations:
            message += "\nRecommended Actions:\n"
            for rec in set(recommendations):
                message += f"- {rec}\n"

        trace_event(
            event="argus_summary_completed",
            context=ctx,
            component="system_summary",
            status="success"
        )

        return self.build_result(
            status="success",
            message=message.strip()
        )