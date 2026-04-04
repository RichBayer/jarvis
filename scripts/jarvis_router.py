#!/usr/bin/env python3

import argparse
import requests
import json

from scripts.query_knowledge import KnowledgeBase


knowledge_base = KnowledgeBase()


def detect_intent(user_request: str) -> str:
    return "knowledge"


# ----------------------------
# NON-STREAMING
# ----------------------------

def query_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200
        }
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    data = response.json()
    return data.get("response", "")


# ----------------------------
# STREAMING (FIXED)
# ----------------------------

def query_ollama_stream(prompt: str):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 200
        }
    }

    response = requests.post(url, json=payload, stream=True)

    if response.status_code != 200:
        yield f"\nError contacting Ollama:\n{response.text}\n"
        return

    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue

        try:
            data = json.loads(line)

            # 🔥 Yield only real text
            chunk = data.get("response", "")

            if chunk:
                yield chunk

            # 🔥 Stop cleanly when done
            if data.get("done"):
                break

        except json.JSONDecodeError:
            continue


# ----------------------------
# PROMPT
# ----------------------------

def build_prompt(user_request: str, context: str) -> str:
    return f"""
You are NeuroCore.

Answer clearly and concisely.

Context:
{context}

Question:
{user_request}

Answer:
"""


# ----------------------------
# ENTRY POINTS
# ----------------------------

def run_query(user_request: str) -> str:
    context = knowledge_base.retrieve(user_request)
    prompt = build_prompt(user_request, context)

    return query_ollama(prompt)


def run_query_stream(user_request: str):
    context = knowledge_base.retrieve(user_request)
    prompt = build_prompt(user_request, context)

    return query_ollama_stream(prompt)


# ----------------------------
# CLI TEST
# ----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    args = parser.parse_args()

    print("\n--- NeuroCore Response ---\n")
    print(run_query(args.request))


if __name__ == "__main__":
    main()