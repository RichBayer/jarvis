#!/usr/bin/env python3

import argparse
import requests
import json

from scripts.query_knowledge import KnowledgeBase
from scripts.session_memory import get_recent_history, add_interaction


knowledge_base = KnowledgeBase()


# ----------------------------
# QUERY REWRITE
# ----------------------------

def rewrite_query(user_request: str) -> str:
    history = get_recent_history()

    if not history:
        return user_request

    last = history[-1]

    prompt = f"""
You are a system that rewrites follow-up questions into fully self-contained technical questions.

Rules:
- Use previous conversation to resolve ambiguity
- Identify the command, tool, or topic explicitly
- Include it clearly in the rewritten question
- Be specific and technical
- Output ONLY the rewritten question

Previous conversation:
User: {last['user']}
Assistant: {last['assistant']}

Follow-up question:
{user_request}

Rewritten question:
"""

    rewritten = query_ollama_once(prompt)

    # Fallback if rewrite fails
    if not rewritten or len(rewritten.split()) < 4:
        return user_request

    return rewritten.strip()


def query_ollama_once(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 100
        }
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return ""
        return response.json().get("response", "").strip()
    except:
        return ""


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
            "num_predict": 600
        }
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"Error: {response.text}"
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"


# ----------------------------
# STREAMING
# ----------------------------

def query_ollama_stream(prompt: str):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 600
        }
    }

    try:
        response = requests.post(url, json=payload, stream=True)

        if response.status_code != 200:
            yield f"\nError contacting Ollama:\n{response.text}\n"
            return

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                data = json.loads(line)
                chunk = data.get("response", "")

                if chunk:
                    yield chunk

                if data.get("done"):
                    break

            except:
                continue

    except Exception as e:
        yield f"\nStreaming error: {e}\n"


# ----------------------------
# PROMPT
# ----------------------------

def build_prompt(user_request: str, context: str) -> str:
    return f"""
You are NeuroCore, a Linux systems assistant.

You MUST base your answer on the provided context.

Rules:
- Use ONLY the provided context
- Do NOT hallucinate or invent details
- Be precise and technical
- When referring to command output fields or column names, use EXACT names from the context

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
    rewritten = rewrite_query(user_request)

    context = knowledge_base.retrieve(rewritten)
    prompt = build_prompt(rewritten, context)

    response = query_ollama(prompt)

    add_interaction(user_request, response)

    return response


def run_query_stream(user_request: str):
    rewritten = rewrite_query(user_request)

    context = knowledge_base.retrieve(rewritten)
    prompt = build_prompt(rewritten, context)

    generator = query_ollama_stream(prompt)

    full_response = ""

    for chunk in generator:
        full_response += chunk
        yield chunk

    add_interaction(user_request, full_response)


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