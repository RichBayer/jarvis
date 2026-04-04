#!/usr/bin/env python3

import socket
import os
import json
import signal
import sys

from runtime.runtime_manager import RuntimeManager
from scripts.jarvis_router import run_query_stream


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
    if "data" in message and isinstance(message["data"], dict):
        input_text = message["data"].get("input")

        if input_text:
            return {
                "type": "query",
                "payload": {
                    "text": input_text
                }
            }

    if "query" in message:
        return {
            "type": "query",
            "payload": {
                "text": message["query"]
            }
        }

    raise ValueError("Invalid request format: no input found")


def recv_full(conn):
    chunks = []
    while True:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            break
        chunks.append(chunk)

    return b"".join(chunks)


def handle_streaming(conn, user_input):
    print(f"\n[Streaming] {user_input}")

    try:
        for chunk in run_query_stream(user_input):
            if chunk:
                conn.sendall(chunk.encode("utf-8"))

        conn.shutdown(socket.SHUT_WR)

    except Exception as e:
        error_msg = f"\nError during streaming: {e}\n"
        try:
            conn.sendall(error_msg.encode("utf-8"))
            conn.shutdown(socket.SHUT_WR)
        except:
            pass


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

            if message.get("stream") is True:
                user_input = normalized["payload"]["text"]
                handle_streaming(conn, user_input)
                continue

            result = runtime.process_request(normalized)

            if isinstance(result, dict) and result.get("status") == "error":
                response = {
                    "status": "error",
                    "response": None,
                    "error": result.get("message")
                }
            else:
                response = {
                    "status": "success",
                    "response": result.get("response") if isinstance(result, dict) else result,
                    "error": None
                }

            conn.sendall(json.dumps(response).encode())
            conn.shutdown(socket.SHUT_WR)

        except Exception as e:
            try:
                error = {
                    "status": "error",
                    "response": None,
                    "error": str(e)
                }
                conn.sendall(json.dumps(error).encode())
                conn.shutdown(socket.SHUT_WR)
            except:
                pass

        finally:
            conn.close()


if __name__ == "__main__":
    main()