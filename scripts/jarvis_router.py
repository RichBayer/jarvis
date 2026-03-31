#!/usr/bin/env python3

"""
NeuroCore Logic Router

Responsibilities:
- Accept a user request
- Detect intent
- Retrieve relevant knowledge (via KnowledgeBase)
- Build prompt
- Send to Ollama via API (streaming)
- Return response (runtime) or print (CLI)

This module supports:
1. CLI usage
2. Runtime usage (via run_query)
"""

import argparse
import requests
import json

from scripts.query_knowledge import KnowledgeBase


# ----------------------------
# GLOBAL (LIGHTWEIGHT) OBJECT
# ----------------------------

knowledge_base = KnowledgeBase()


def detect_intent(user_request: str) -> str:
    request = user_request.lower()

    for word in ["what", "how", "explain", "tell", "find", "search", "describe"]:
        if word in request:
            return "knowledge"

    return "knowledge"


def query_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 200
        }
    }

    try:
        response = requests.post(url, json=payload, stream=True)

        if response.status_code != 200:
            print("Error contacting Ollama:\n")
            print(response.text)
            return ""

        output = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))

                    if "response" in data:
                        chunk = data["response"]
                        print(chunk, end="", flush=True)
                        output += chunk

                except json.JSONDecodeError:
                    continue

        print()
        return output

    except Exception as e:
        print(f"Error during Ollama request: {e}")
        return ""


def build_prompt(user_request: str, context: str) -> str:
    return f"""
You are NeuroCore, a local-first AI assistant.

You were previously known as Jarvis. Some internal systems and older documentation may still reference that name.

Answer concisely and clearly.

Context:
{context}

Question:
{user_request}

Answer:
"""


def run_query(user_request: str) -> str:
    """
    Runtime entry point.
    """

    intent = detect_intent(user_request)

    if intent == "knowledge":
        context = knowledge_base.retrieve(user_request)
        prompt = build_prompt(user_request, context)

        return query_ollama(prompt)

    return "No valid intent detected."


def main():
    parser = argparse.ArgumentParser(description="NeuroCore Logic Router")
    parser.add_argument("request", help="User request")

    args = parser.parse_args()

    print("\n--- NeuroCore Response ---\n")

    run_query(args.request)


if __name__ == "__main__":
    main()