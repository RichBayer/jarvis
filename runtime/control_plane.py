# /mnt/g/ai/projects/neurocore/runtime/control_plane.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from tools.execution_engine import ExecutionEngine
from tools.tool_registry import registry
from runtime.tracing import trace_event, trace_context_from_request


@dataclass
class AuthorizedRequest:
    normalized_input: str
    session_memory_allowed: bool = True
    external_input_present: bool = False

    class RequestClass:
        value = "reasoning"

    request_class = RequestClass()


class ControlPlane:

    EXECUTION_KEYWORDS = {
        "start", "stop", "restart", "status",
        "info", "processes", "disk", "memory",
        "layout", "network", "connections",
        "uptime", "logs", "users", "logins",
        # Argus keywords
        "summary"
    }

    CONFIRM_PREFIX = "confirm "

    def __init__(self) -> None:
        self.execution_engine = ExecutionEngine()

    def authorize(self, request: Dict[str, Any]) -> AuthorizedRequest:
        ctx = trace_context_from_request(request)
        text = request.get("data", {}).get("input", "")

        trace_event(
            event="authorize_called",
            context=ctx,
            component="control_plane",
            details={"input": text}
        )

        authorized = AuthorizedRequest(normalized_input=text)

        trace_event(
            event="authorize_completed",
            context=ctx,
            component="control_plane",
            status="success"
        )

        return authorized

    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ctx = trace_context_from_request(request)
        query = request.get("query", "").strip()

        trace_event(
            event="process_started",
            context=ctx,
            component="control_plane",
            details={"query": query}
        )

        if not self._is_execution_request(request):
            return {
                "status": "pass_through",
                "message": "Not execution",
            }

        confirmed = self._is_confirmed(query)
        cleaned_query = self._strip_confirm(query)

        structured = self._build_execution_request({"query": cleaned_query})

        if "trace" in request:
            structured["trace"] = request["trace"]

        tool = registry.get(structured["tool"])

        if not tool:
            return {
                "status": "error",
                "message": f"Tool '{structured['tool']}' not found",
            }

        if tool.execution_mode == "manual" and not confirmed:
            return {
                "status": "confirmation_required",
                "tool": tool.name,
                "message": f"Tool '{tool.name}' requires confirmation",
            }

        return self.execution_engine.execute(structured)

    def _is_execution_request(self, request: Dict[str, Any]) -> bool:
        text = request.get("query", "").lower().strip()
        text = self._strip_confirm(text)
        words = text.split()
        return bool(words and words[0] in self.EXECUTION_KEYWORDS)

    def _is_confirmed(self, query: str) -> bool:
        return query.lower().startswith(self.CONFIRM_PREFIX)

    def _strip_confirm(self, query: str) -> str:
        if query.lower().startswith(self.CONFIRM_PREFIX):
            return query[len(self.CONFIRM_PREFIX):].strip()
        return query

    def _build_execution_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        words = request.get("query", "").lower().split()

        action = words[0] if len(words) > 0 else ""

        # -------------------------
        # ARGUS TOOL MAPPING (NEW)
        # -------------------------
        if action == "summary":
            return {"tool": "system_summary", "input": {}}

        # -------------------------
        # SYSTEM TOOL MAPPING
        # -------------------------
        if action == "logins":
            return {"tool": "recent_logins", "input": {}}
        if action == "users":
            return {"tool": "users_sessions", "input": {}}
        if action == "logs":
            return {"tool": "system_logs", "input": {}}
        if action == "uptime":
            return {"tool": "uptime_load", "input": {}}
        if action == "connections":
            return {"tool": "network_connections", "input": {}}
        if action == "network":
            return {"tool": "network_interfaces", "input": {}}
        if action == "layout":
            return {"tool": "disk_layout", "input": {}}
        if action == "memory":
            return {"tool": "memory_usage", "input": {}}
        if action == "disk":
            return {"tool": "disk_usage", "input": {}}
        if action == "processes":
            return {"tool": "process_top", "input": {}}
        if action == "info":
            return {"tool": "system_info", "input": {"target": "system"}}

        # fallback
        return {
            "tool": "service_manager",
            "input": {}
        }