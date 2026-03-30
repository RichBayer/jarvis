#!/usr/bin/env python3

import socket
import os
import json
import signal
import sys

SOCKET_PATH = "/tmp/neurocore.sock"


def cleanup():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)


def handle_exit(signum, frame):
    print("\nShutting down NeuroCore daemon...")
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def main():
    cleanup()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    print(f"NeuroCore daemon listening on {SOCKET_PATH}")

    while True:
        conn, _ = server.accept()

        try:
            data = conn.recv(4096)

            if not data:
                conn.close()
                continue

            message = json.loads(data.decode())

            print("\n--- Incoming Request ---")
            print(json.dumps(message, indent=2))

            # Structured response (aligned with your architecture)
            response = {
                "status": "ok",
                "type": message.get("type", "unknown"),
                "response": "NeuroCore daemon received request"
            }

            conn.sendall(json.dumps(response).encode())

        except Exception as e:
            error = {"status": "error", "message": str(e)}
            conn.sendall(json.dumps(error).encode())

        finally:
            conn.close()


if __name__ == "__main__":
    main()