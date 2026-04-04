#!/usr/bin/env python3

import sys
import socket
import json

SOCKET_PATH = "/tmp/neurocore.sock"
BUFFER_SIZE = 4096
TIMEOUT = 60


def send_request(request, stream=False):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(TIMEOUT)

    try:
        client.connect(SOCKET_PATH)

        # Send request
        client.sendall(json.dumps(request).encode("utf-8"))

        # Signal end of request
        client.shutdown(socket.SHUT_WR)

        # STREAMING MODE
        if stream:
            while True:
                chunk = client.recv(BUFFER_SIZE)
                if not chunk:
                    break

                print(chunk.decode("utf-8"), end="", flush=True)

            print()
            return None

        # NON-STREAM MODE (fallback)
        chunks = []
        while True:
            chunk = client.recv(BUFFER_SIZE)
            if not chunk:
                break
            chunks.append(chunk)

        response_data = b"".join(chunks).decode("utf-8")
        return json.loads(response_data)

    finally:
        client.close()


def build_request(user_input):
    return {
        "type": "query",
        "user": "richard",
        "mode": "cli",
        "stream": True,  # 🔥 always stream now
        "data": {
            "input": user_input
        }
    }


def interactive_mode():
    print("\nNeuroCore Interactive Mode")
    print("Type 'exit' or 'quit' to leave\n")

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting NeuroCore...")
                break

            request = build_request(user_input)
            send_request(request, stream=True)

        except KeyboardInterrupt:
            print("\nExiting NeuroCore...")
            break

        except Exception as e:
            print(f"CLI Error: {e}", file=sys.stderr)


def main():
    # If arguments provided → one-shot mode
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        request = build_request(user_input)

        try:
            send_request(request, stream=True)

        except socket.timeout:
            print("Error: NeuroCore is initializing. Try again.", file=sys.stderr)
            sys.exit(1)

        except Exception as e:
            print(f"CLI Error: {e}", file=sys.stderr)
            sys.exit(1)

    # No arguments → interactive mode
    else:
        interactive_mode()


if __name__ == "__main__":
    main()