# /mnt/g/ai/projects/neurocore/runtime/runtime_manager.py

from scripts.jarvis_router import run_authorized_query, run_authorized_stream_query
from runtime.control_plane import ControlPlane
import re


def is_ambiguous(query: str) -> bool:
    q = query.lower().strip()
    q = re.sub(r"[^\w\s]", "", q)

    words = q.split()

    vague_words = {"what", "does", "that", "mean", "it", "this", "explain"}

    return len(words) <= 5 and all(w in vague_words for w in words)


def no_context_response() -> str:
    return (
        "I do not have enough context to know what you're referring to. "
        "Please include the specific command output, error message, or topic you want explained."
    )


def format_execution_result(result: dict) -> str:
    status = result.get("status")
    message = result.get("message", "")
    data = result.get("data", {})

    if status == "success":
        action = data.get("action", "")
        service = data.get("service", "")
        return f"[OK] {action.upper()} '{service}' → {message}"

    if status == "confirmation_required":
        return (
            f"[CONFIRMATION REQUIRED] {message}\n"
            f"Run: {data.get('confirm_command')}"
        )

    if status == "policy_denied":
        return f"[BLOCKED] {message}"

    if status == "error":
        return f"[ERROR] {message}"

    return str(result)


class RuntimeManager:
    def __init__(self):
        print("Initializing NeuroCore Runtime Manager...")
        self.control_plane = ControlPlane()

    def handle_request(self, request):
        raw_input = request.get("data", {}).get("input", "")

        if is_ambiguous(raw_input):
            return no_context_response()

        if self.control_plane._is_execution_request({"query": raw_input}):
            result = self.control_plane.process({"query": raw_input})
            return format_execution_result(result)

        authorized = self.control_plane.authorize(request)
        return run_authorized_query(authorized)

    def handle_stream_request(self, request):
        raw_input = request.get("data", {}).get("input", "")

        if is_ambiguous(raw_input):
            yield no_context_response()
            return

        if self.control_plane._is_execution_request({"query": raw_input}):
            result = self.control_plane.process({"query": raw_input})
            yield format_execution_result(result) + "\n"
            return

        authorized = self.control_plane.authorize(request)

        for chunk in run_authorized_stream_query(authorized):
            yield chunk