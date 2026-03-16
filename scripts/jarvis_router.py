#!/usr/bin/env python3

"""
Jarvis Logic Router

Initial logic layer component for the Jarvis AI system.

Responsibilities:
- Accept a user request
- Detect intent
- Route knowledge requests to the knowledge retrieval tool
- Assemble a prompt with retrieved context
- Send the prompt to the local Ollama model
"""

import argparse
import subprocess

from query_knowledge import retrieve_knowledge


def detect_intent(user_request: str) -> str:
    """
    Simple rule-based intent detection.
    For now almost everything routes to the knowledge system.
    """

    request = user_request.lower()

    knowledge_triggers = [
        "what",
        "how",
        "explain",
        "tell me",
        "find",
        "search"
    ]

    for trigger in knowledge_triggers:
        if trigger in request:
            return "knowledge"

    return "knowledge"


def main():

    parser = argparse.ArgumentParser(description="Jarvis Logic Router")
    parser.add_argument("request", help="User request")

    args = parser.parse_args()

    intent = detect_intent(args.request)

    if intent == "knowledge":

        context = retrieve_knowledge(args.request)

        prompt = f"""
You are Jarvis, a local AI assistant.

Use the following context to answer the user's question.

Context:
{context}

Question:
{args.request}

Answer:
"""

        print("\n--- Constructed Prompt ---\n")
        print(prompt)

        print("\n--- Jarvis Response ---\n")

        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b"],
            input=prompt,
            text=True,
            capture_output=True
        )

        print(result.stdout)


if __name__ == "__main__":
    main()