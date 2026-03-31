#!/usr/bin/env python3

"""
NeuroCore Daemon

Responsibilities:
- Run as a persistent background process
- Accept incoming client connections via UNIX socket
- Receive structured JSON requests
- Pass requests to Runtime Manager
- Return structured responses

This daemon serves as the central communication layer for NeuroCore.

Architecture:

Client → UNIX Socket → Daemon → Runtime Manager → Router → Response → Client
"""

import socket
import os
import json
import signal
import sys

from runtime.runtime_manager import RuntimeManager


SOCKET_PATH = "/tmp/neurocore.sock"


def cleanup():
    """
    Remove socket file on shutdown to prevent conflicts.
    """
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)


def handle_exit(signum, frame):
    """
    Handle graceful shutdown.
    """
    print("\nShutting down NeuroCore daemon...")
    cleanup()
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def main():
    """
    Entry point for NeuroCore daemon.
    """

    # Ensure no stale socket exists
    cleanup()

    # Create UNIX socket server
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    print(f"NeuroCore daemon listening on {SOCKET_PATH}")

    # Initialize runtime manager ONCE (persistent system state)
    runtime = RuntimeManager()

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

            # Pass request to runtime manager
            response = runtime.process_request(message)

            # Send response back to client
            conn.sendall(json.dumps(response).encode())

        except Exception as e:
            error = {
                "status": "error",
                "message": str(e)
            }
            conn.sendall(json.dumps(error).encode())

        finally:
            conn.close()


if __name__ == "__main__":
    main()