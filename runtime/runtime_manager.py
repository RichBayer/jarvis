#!/usr/bin/env python3

"""
NeuroCore Runtime Manager

Responsibilities:
- Manage persistent system state
- Process incoming requests from daemon
- Route queries to logic layer (router)
- Return structured responses
"""

from scripts.jarvis_router import run_query


class RuntimeManager:
    def __init__(self):
        """
        Initialize runtime components.
        """
        print("Initializing NeuroCore Runtime Manager...")

    def process_request(self, request: dict) -> dict:
        """
        Process a structured request.

        Expected format:
        {
            "type": "query",
            "payload": {
                "text": "..."
            }
        }
        """

        try:
            request_type = request.get("type")

            if request_type == "query":
                return self._handle_query(request)

            return {
                "status": "error",
                "message": f"Unsupported request type: {request_type}"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _handle_query(self, request: dict) -> dict:
        """
        Handle query-type requests.
        """

        payload = request.get("payload", {})
        user_input = payload.get("text", "")

        if not user_input:
            return {
                "status": "error",
                "message": "No query text provided"
            }

        print(f"\n[Runtime] Processing query: {user_input}")

        response_text = run_query(user_input)

        return {
            "status": "ok",
            "type": "query",
            "response": response_text
        }