#!/usr/bin/env python3

import json
import requests
import re

from scripts.session_memory import add_interaction

# ----------------------------
# AMBIGUITY DETECTION (FINAL)
# ----------------------------

def is_ambiguous(query: str) -> bool:
    q = query.lower().strip()

    # Remove punctuation
    q = re.sub(r"[^\w\s]", "", q)

    # Tokenize
    words = q.split()

    # 🔥 Core logic:
    # Very short + vague queries = ambiguous
    if len(words) <= 5:
        vague_words = {"what", "does", "that", "mean", "it", "this", "explain"}
        if all(w in vague_words for w in words):
            return True

    return False


def no_context_response() -> str:
    return (
        "I do not have enough context to know what you're referring to. "
        "Please include the specific command output, error message, or topic you want explained."
    )


# ----------------------------
# MODEL CALLS
# ----------------------------

def query_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 600},
    }

    response = requests.post(url, json=payload)
    return response.json().get("response", "")


def query_ollama_stream(prompt: str):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": True,
        "options": {"num_predict": 600},
    }

    response = requests.post(url, json=payload, stream=True)

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


# ----------------------------
# PROMPTS
# ----------------------------

def build_prompt(user_request: str) -> str:
    return f"""
You are NeuroCore, a Linux systems assistant.

Answer clearly and technically.

Question:
{user_request}

Answer:
"""


def build_analysis_prompt(user_input: str) -> str:
    return f"""
You are analyzing raw system output.

Rules:
- ONLY describe what is directly observable
- DO NOT guess meaning
- DO NOT infer purpose

Input:
{user_input}

Analysis:
"""


# ----------------------------
# CORE EXECUTION
# ----------------------------

def run_authorized_query(authorized) -> str:
    user_request = authorized.normalized_input

    # PIPE MODE
    if authorized.external_input_present:
        return query_ollama(build_analysis_prompt(user_request))

    # 🔥 FINAL ambiguity guard
    if is_ambiguous(user_request):
        return no_context_response()

    response = query_ollama(build_prompt(user_request))

    if authorized.session_memory_allowed:
        add_interaction(user_request, response)

    return response


def run_authorized_stream_query(authorized):
    user_request = authorized.normalized_input

    if authorized.external_input_present:
        for chunk in query_ollama_stream(build_analysis_prompt(user_request)):
            yield chunk
        return

    if is_ambiguous(user_request):
        yield no_context_response()
        return

    full = ""

    for chunk in query_ollama_stream(build_prompt(user_request)):
        full += chunk
        yield chunk

    if authorized.session_memory_allowed:
        add_interaction(user_request, full)