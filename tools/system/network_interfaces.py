# /mnt/g/ai/projects/neurocore/tools/system/network_interfaces.py

from __future__ import annotations
from typing import Dict, Any, List

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class NetworkInterfaces(BaseTool):

    name = "network_interfaces"
    description = "Retrieve network interface information"
    execution_mode = "auto"

    input_schema = {"required": []}

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="network_interfaces_collection_started",
            context=ctx,
            component="network_interfaces"
        )

        result = CommandRunner.run(["ip", "a"])
        parsed = self._parse_ip_output(result.get("stdout", ""))

        data = {
            "interfaces": parsed,
            "raw": result
        }

        trace_event(
            event="network_interfaces_execution_completed",
            context=ctx,
            component="network_interfaces",
            status="success"
        )

        return self.build_result(
            status="success",
            message="Network interfaces collected",
            data=data
        )

    # -------------------------
    # PARSER
    # -------------------------

    def _parse_ip_output(self, output: str) -> List[Dict[str, Any]]:
        lines = output.splitlines()

        interfaces = []
        current = None

        for line in lines:
            line = line.strip()

            # Interface line
            if line and line[0].isdigit():
                parts = line.split(":", 2)

                if len(parts) < 2:
                    continue

                name = parts[1].strip().split("@")[0]
                state = "UNKNOWN"

                if "state UP" in line:
                    state = "UP"
                elif "state DOWN" in line:
                    state = "DOWN"

                current = {
                    "name": name,
                    "state": state,
                    "mac": None,
                    "ipv4": [],
                    "ipv6": []
                }

                interfaces.append(current)
                continue

            if current is None:
                continue

            # MAC address
            if line.startswith("link/"):
                parts = line.split()
                if len(parts) >= 2:
                    current["mac"] = parts[1]

            # IPv4
            elif line.startswith("inet "):
                parts = line.split()
                if len(parts) >= 2:
                    current["ipv4"].append(parts[1])

            # IPv6
            elif line.startswith("inet6 "):
                parts = line.split()
                if len(parts) >= 2:
                    current["ipv6"].append(parts[1])

        return interfaces