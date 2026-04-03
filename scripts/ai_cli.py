import sys
import socket
import json

SOCKET_PATH = "/tmp/neurocore.sock"
BUFFER_SIZE = 4096
TIMEOUT = 60


def send_request(request):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(TIMEOUT)

    try:
        client.connect(SOCKET_PATH)

        # Send request
        client.sendall(json.dumps(request).encode("utf-8"))

        # 🔥 CRITICAL FIX: signal end of request
        client.shutdown(socket.SHUT_WR)

        # Receive response
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
        "data": {
            "input": user_input
        }
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: ai \"your query\"")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    request = build_request(user_input)

    try:
        response = send_request(request)

        if response.get("status") == "success":
            print(response.get("response", ""))
        else:
            print(response.get("error", "Unknown error"), file=sys.stderr)

    except socket.timeout:
        print("Error: NeuroCore is initializing (first query may take longer). Try again.", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"CLI Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()