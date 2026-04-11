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
    """
    Normalize incoming client messages into the runtime request shape.

    Important:
    We preserve current CLI compatibility while adding the source hint
    needed by the control plane.
    """
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
        # Current CLI does not explicitly send source. Use mode as the best available hint.
        source = "cli_pipe" if mode == "pipe" else "cli_direct"

    return {
        "type": "query",
        "user": message.get("user", "richard"),
        "mode": mode,
        "stream": message.get("stream", False),
        "source": source,
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

            if normalized.get("stream") is True:
                for chunk in runtime.handle_stream_request(normalized):
                    if chunk:
                        conn.sendall(chunk.encode("utf-8"))

                conn.shutdown(socket.SHUT_WR)
                continue

            result = runtime.handle_request(normalized)

            response = {
                "status": "success",
                "response": result,
                "error": None
            }

            conn.sendall(json.dumps(response).encode())
            conn.shutdown(socket.SHUT_WR)

        except Exception as e:
            error = {
                "status": "error",
                "response": None,
                "error": str(e)
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