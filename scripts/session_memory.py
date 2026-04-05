#!/usr/bin/env python3

import json
import os

SESSION_FILE = "/mnt/g/ai/memory/sessions/richard/session.json"
MAX_HISTORY = 5


def load_session():
    if not os.path.exists(SESSION_FILE):
        return []

    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_session(history):
    trimmed = history[-MAX_HISTORY:]

    with open(SESSION_FILE, "w") as f:
        json.dump(trimmed, f, indent=2)


def add_interaction(user_input, response):
    history = load_session()

    history.append({
        "user": user_input,
        "assistant": response
    })

    save_session(history)


def get_recent_history():
    return load_session()