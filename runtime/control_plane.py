from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict
import re


class SourceType(str, Enum):
    CLI_DIRECT = "cli_direct"
    CLI_PIPE = "cli_pipe"
    CLI_INTERACTIVE = "cli_interactive"


class RequestClass(str, Enum):
    CONVERSATIONAL = "conversational"
    KNOWLEDGE = "knowledge"
    EXTERNAL_INPUT = "external_input"
    EXECUTION_INTENT = "execution_intent"


class OperatingMode(str, Enum):
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    EXECUTION_CANDIDATE = "execution_candidate"


@dataclass
class AuthorizedRequest:
    normalized_input: str
    source: SourceType
    request_class: RequestClass
    mode: OperatingMode
    session_memory_allowed: bool
    retrieval_allowed: bool
    external_input_present: bool


class ControlPlane:
    """
    Phase 5A control-plane skeleton.

    Responsibilities:
    - classify request source
    - classify request type
    - assign operating mode
    - grant or deny memory / retrieval usage
    - detect execution intent without executing anything
    """

    EXECUTION_PATTERNS = [
        r"^\s*(run|execute|restart|stop|start|kill|delete|remove|rm|shutdown|reboot|install|uninstall|create|index|backup|snapshot)\b",
        r"^\s*(apt|apt-get|dnf|yum|systemctl|service|rm|mv|cp|chmod|chown|docker|podman|kubectl)\b",
    ]

    KNOWLEDGE_HINTS = [
        "what",
        "how",
        "why",
        "explain",
        "describe",
        "define",
    ]

    def authorize(self, request: Dict[str, Any]) -> AuthorizedRequest:
        user_input = self._extract_input(request)
        source = self._detect_source(request)
        request_class = self._classify(user_input, source)
        mode = self._select_mode(request_class)

        session_memory_allowed = mode == OperatingMode.REASONING
        retrieval_allowed = mode == OperatingMode.REASONING
        external_input_present = source == SourceType.CLI_PIPE

        return AuthorizedRequest(
            normalized_input=user_input,
            source=source,
            request_class=request_class,
            mode=mode,
            session_memory_allowed=session_memory_allowed,
            retrieval_allowed=retrieval_allowed,
            external_input_present=external_input_present,
        )

    def _extract_input(self, request: Dict[str, Any]) -> str:
        if "data" in request and isinstance(request["data"], dict):
            text = request["data"].get("input")
            if isinstance(text, str) and text.strip():
                return text.strip()

        if "payload" in request and isinstance(request["payload"], dict):
            text = request["payload"].get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()

        if "query" in request and isinstance(request["query"], str) and request["query"].strip():
            return request["query"].strip()

        raise ValueError("Invalid request format: no input found")

    def _detect_source(self, request: Dict[str, Any]) -> SourceType:
        source = request.get("source")
        mode = request.get("mode")

        if source == "cli_pipe" or mode == "pipe":
            return SourceType.CLI_PIPE

        if mode == "interactive":
            return SourceType.CLI_INTERACTIVE

        return SourceType.CLI_DIRECT

    def _classify(self, text: str, source: SourceType) -> RequestClass:
        lowered = text.lower()

        if source == SourceType.CLI_PIPE:
            return RequestClass.EXTERNAL_INPUT

        if self._is_execution_intent(lowered):
            return RequestClass.EXECUTION_INTENT

        if any(hint in lowered for hint in self.KNOWLEDGE_HINTS):
            return RequestClass.KNOWLEDGE

        return RequestClass.CONVERSATIONAL

    def _select_mode(self, request_class: RequestClass) -> OperatingMode:
        if request_class == RequestClass.EXTERNAL_INPUT:
            return OperatingMode.ANALYSIS

        if request_class == RequestClass.EXECUTION_INTENT:
            return OperatingMode.EXECUTION_CANDIDATE

        return OperatingMode.REASONING

    def _is_execution_intent(self, text: str) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in self.EXECUTION_PATTERNS)