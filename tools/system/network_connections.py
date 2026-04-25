# /mnt/g/ai/projects/neurocore/tools/system/network_connections.py

from __future__ import annotations
from typing import Dict, Any, List

from runtime.tracing import trace_event, trace_context_from_request
from tools.base_tool import BaseTool
from tools.system.command_runner import CommandRunner


class NetworkConnections(BaseTool):

    name = "network_connections"
    description = "Retrieve active network connections"
    execution_mode = "auto"

    input_schema = {"required": []}

    def validate_input(self, tool_input: Dict) -> None:
        return

    def execute(self, request: Dict) -> Dict:
        ctx = trace_context_from_request(request)

        trace_event(
            event="network_connections_collection_started",
            context=ctx,
            component="network_connections"
        )

        result = CommandRunner.run(["ss", "-tulnp"])
        parsed = self._parse_ss_output(result.get("stdout", ""))

        data = {
            "connections": parsed,
            "raw": result
        }

        trace_event(
            event="network_connections_execution_completed",
            context=ctx,
            component="network_connections",
            status="success"
        )

        return self.build_result(
            status="success",
            message="Network connections collected",
            data=data
        )

    # -------------------------
    # PARSER
    # -------------------------

    def _parse_ss_output(self, output: str) -> List[Dict[str, Any]]:
        lines = output.splitlines()

        if len(lines) < 2:
            return []

        rows = lines[1:]
        parsed = []

        for row in rows:
            parts = row.split()

            if len(parts) < 5:
                continue

            try:
                protocol = parts[0]
                state = parts[1]

                local = parts[4]
                peer = parts[5] if len(parts) > 5 else "*"

                process = parts[-1] if "users:" in row else None

                local_addr, local_port = self._split_address(local)
                peer_addr, peer_port = self._split_address(peer)

                parsed.append({
                    "protocol": protocol,
                    "state": state,
                    "local_address": local_addr,
                    "local_port": local_port,
                    "peer_address": peer_addr,
                    "peer_port": peer_port,
                    "process": process
                })

            except Exception:
                continue

        return parsed

    def _split_address(self, value: str):
        if ":" in value:
            parts = value.rsplit(":", 1)
            return parts[0], parts[1]
        return value, None