#!/usr/bin/env python3

"""
NeuroCore Logic Router (API + Streaming)

Responsibilities:
- Accept a user request
- Detect intent
- Retrieve relevant knowledge
- Build prompt
- Send to Ollama via API (streaming)
- Display response in real-time
"""

import argparse
import requests
import json

from query_knowledge import retrieve_knowledge


def detect_intent(user_request: str) -> str:
    """
    Simple rule-based intent detection.
    Currently defaults to knowledge.
    """
    request = user_request.lower()

    for word in ["what", "how", "explain", "tell", "find", "search", "describe"]:
        if word in request:
            return "knowledge"

    return "knowledge"


def query_ollama(prompt: str) -> str:
    """
    Send prompt to Ollama API using streaming response.
    """

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 200  # limits response size for speed
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

        print()  # newline after streaming completes
        return output

    except Exception as e:
        print(f"Error during Ollama request: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(description="NeuroCore Logic Router")
    parser.add_argument("request", help="User request")

    args = parser.parse_args()

    intent = detect_intent(args.request)

    if intent == "knowledge":

        context = retrieve_knowledge(args.request)

        # Optional debug (uncomment if needed)
        # print(f"\n--- Context Length: {len(context)} chars ---\n")

        prompt = f"""
You are NeuroCore, a local-first AI assistant.

You were previously known as Jarvis. Some internal systems and older documentation may still reference that name.

Answer concisely and clearly.

Context:
{context}

Question:
{args.request}

Answer:
"""

        print("\n--- Constructed Prompt ---\n")
        print(prompt)

        print("\n--- NeuroCore Response ---\n")

        query_ollama(prompt)


if __name__ == "__main__":
    main()