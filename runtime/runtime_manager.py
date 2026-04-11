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


class RuntimeManager:
    def __init__(self):
        print("Initializing NeuroCore Runtime Manager...")
        self.control_plane = ControlPlane()

    def handle_request(self, request):
        # 🔥 USE RAW INPUT — NOT normalized
        raw_input = request.get("payload", {}).get("text", "")

        # 🔥 HARD GUARD BEFORE ANY PROCESSING
        if is_ambiguous(raw_input):
            return no_context_response()

        authorized = self.control_plane.authorize(request)

        if authorized.request_class.value == "execution_intent":
            return self._downgrade_execution(authorized)

        return run_authorized_query(authorized)

    def handle_stream_request(self, request):
        # 🔥 USE RAW INPUT — NOT normalized
        raw_input = request.get("payload", {}).get("text", "")

        # 🔥 HARD GUARD BEFORE ANY PROCESSING
        if is_ambiguous(raw_input):
            yield no_context_response()
            return

        authorized = self.control_plane.authorize(request)

        if authorized.request_class.value == "execution_intent":
            yield "[Control Plane] Execution not allowed.\n\n"
            yield self._downgrade_execution(authorized)
            return

        for chunk in run_authorized_stream_query(authorized):
            yield chunk

    def _downgrade_execution(self, authorized):
        advisory_prompt = (
            "The user requested an action, but NeuroCore does not execute commands.\n"
            "Provide safe, manual instructions only.\n\n"
            f"User request: {authorized.normalized_input}"
        )

        class Advisory:
            def __init__(self, text):
                self.normalized_input = text
                self.session_memory_allowed = False
                self.external_input_present = False

        return run_authorized_query(Advisory(advisory_prompt))