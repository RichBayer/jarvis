# /mnt/g/ai/projects/neurocore/runtime/control_plane.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from tools.execution_engine import ExecutionEngine
from tools.tool_registry import registry


@dataclass
class AuthorizedRequest:
    normalized_input: str
    session_memory_allowed: bool = True
    external_input_present: bool = False

    class RequestClass:
        value = "reasoning"

    request_class = RequestClass()


class ControlPlane:

    EXECUTION_KEYWORDS = {"start", "stop", "restart", "status"}
    CONFIRM_PREFIX = "confirm "

    def __init__(self) -> None:
        self.execution_engine = ExecutionEngine()

    # -------------------------
    # REASONING COMPATIBILITY
    # -------------------------

    def authorize(self, request: Dict[str, Any]) -> AuthorizedRequest:
        text = request.get("data", {}).get("input", "")
        return AuthorizedRequest(normalized_input=text)

    # -------------------------
    # MAIN ENTRY
    # -------------------------

    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        query = request.get("query", "").strip()

        if not self._is_execution_request({"query": query}):
            return {
                "status": "pass_through",
                "message": "Not execution",
            }

        confirmed = self._is_confirmed(query)
        cleaned_query = self._strip_confirm(query)

        structured = self._build_execution_request({"query": cleaned_query})

        tool = registry.get(structured["tool"])

        if not tool:
            return {
                "status": "error",
                "error_type": "tool_not_found",
                "message": f"Tool '{structured['tool']}' not found",
            }

        # 🔥 POLICY ENFORCEMENT
        mode = tool.execution_mode

        if mode == "manual" and not confirmed:
            return {
                "status": "confirmation_required",
                "tool": tool.name,
                "message": f"Tool '{tool.name}' requires confirmation",
                "data": {
                    "confirm_command": f'ai "confirm {cleaned_query}"'
                },
            }

        if mode == "dry-run":
            return {
                "status": "policy_denied",
                "message": "Tool is dry-run only",
            }

        # 🔥 EXECUTE
        return self.execution_engine.execute(structured)

    # -------------------------
    # HELPERS
    # -------------------------

    def _is_execution_request(self, request: Dict[str, Any]) -> bool:
        text = request.get("query", "").lower().strip()
        if not text:
            return False

        text = self._strip_confirm(text)
        words = text.split()

        if not words:
            return False

        return words[0] in self.EXECUTION_KEYWORDS

    def _is_confirmed(self, query: str) -> bool:
        return query.lower().startswith(self.CONFIRM_PREFIX)

    def _strip_confirm(self, query: str) -> str:
        if query.lower().startswith(self.CONFIRM_PREFIX):
            return query[len(self.CONFIRM_PREFIX):].strip()
        return query

    def _build_execution_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        words = request.get("query", "").lower().split()

        action = words[0] if len(words) > 0 else ""
        service = words[1] if len(words) > 1 else ""

        return {
            "tool": "service_manager",
            "input": {
                "action": action,
                "service": service,
            },
        }