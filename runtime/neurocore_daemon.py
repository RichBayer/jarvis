#!/usr/bin/env python3

import socket
import os
import json
import signal
import sys

from runtime.runtime_manager import RuntimeManager


SOCKET_PATH = "/tmp/neurocore.sock"
BUFFER_SIZE = 4096


def cleanup():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)


def handle_exit(signum, frame):
    print("\nShutting down NeuroCore daemon...")
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def normalize_request(message):
    input_text = None

    if "data" in message and isinstance(message["data"], dict):
        input_text = message["data"].get("input")

    if not input_text and "query" in message:
        input_text = message["query"]

    if not input_text:
        raise ValueError("Invalid request format: no input found")

    source = message.get("source")
    mode = message.get("mode", "cli")

    if source is None:
        source = "cli_pipe" if mode == "pipe" else "cli_direct"

    trace = message.get("trace")

    return {
        "type": "query",
        "user": message.get("user", "richard"),
        "mode": mode,
        "stream": True,  # force unified handling
        "source": source,
        "trace": trace,
        "data": {
            "input": input_text
        }
    }


def recv_full(conn):
    chunks = []
    while True:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            break
        chunks.append(chunk)
    return b"".join(chunks)


def main():
    cleanup()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    print(f"NeuroCore daemon listening on {SOCKET_PATH}")

    runtime = RuntimeManager()

    while True:
        conn, _ = server.accept()

        try:
            raw_data = recv_full(conn)

            if not raw_data:
                conn.close()
                continue

            message = json.loads(raw_data.decode())

            print("\n--- Incoming Request ---")
            print(json.dumps(message, indent=2))

            normalized = normalize_request(message)

            # ✅ unified execution path
            response = runtime.handle_stream_request(normalized)

            conn.sendall(json.dumps(response).encode())
            conn.shutdown(socket.SHUT_WR)

        except Exception as e:
            error = {
                "status": "error",
                "response": None,
                "error": str(e),
                "data": {}
            }
            try:
                conn.sendall(json.dumps(error).encode())
                conn.shutdown(socket.SHUT_WR)
            except Exception:
                pass

        finally:
            conn.close()


if __name__ == "__main__":
    main()