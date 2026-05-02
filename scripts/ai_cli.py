#!/usr/bin/env python3

import sys
import json
import socket
import uuid
import argparse

SOCKET_PATH = "/tmp/neurocore.sock"


def build_trace(source: str) -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "source": source,
        "metadata": {}
    }


# -------------------------
# CLI ARGUMENT PARSING
# -------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog="ai",
        description="NeuroCore CLI interface"
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Query to send to NeuroCore"
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Show raw evidence for Argus diagnostic output"
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary-only Argus diagnostic output"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON response from NeuroCore"
    )

    return parser.parse_args()


# -------------------------
# ARGUS FORMATTER
# -------------------------

def clean_title(output):
    title = output or "Argus Diagnostic Output"

    if title.startswith("[OK] "):
        title = title.replace("[OK] ", "", 1)

    if "[" in title:
        title = title.split("[")[0].strip()

    if not title:
        title = "Argus Diagnostic Output"

    return title


def print_findings(findings):
    if not findings:
        print("Findings:")
        print("- None")
        print()
        return

    print("Findings:")

    for finding in findings:
        if isinstance(finding, dict):
            message = finding.get("message", str(finding))
        else:
            message = str(finding)

        print(f"- {message}")

    print()


def print_recommendations(recommendations):
    print("Recommendations:")

    if recommendations:
        for recommendation in recommendations:
            print(f"- {recommendation}")
    else:
        print("- None")

    print()


def print_raw_evidence(raw):
    if not isinstance(raw, dict) or not raw:
        print("--- RAW OUTPUT ---")
        print()
        print("No raw evidence available.")
        return

    print("--- RAW OUTPUT ---")

    for section, value in raw.items():
        print(f"\n[{section.upper()}]")

        if isinstance(value, dict):
            for _, sub_value in value.items():
                print(sub_value)
        else:
            print(value)


def print_raw_hint(user_input, raw_available):
    if not raw_available:
        return

    print("Raw evidence hidden by default.")
    print("To inspect raw evidence, run:")
    print(f'ai --raw "{user_input}"')


def format_argus_output(
    output,
    data,
    user_input,
    show_raw=False,
    summary_only=False
):
    severity = data.get("severity", "UNKNOWN")
    findings = data.get("findings", [])
    recommendations = data.get("recommendations", [])
    raw = data.get("raw", {})

    title = clean_title(output)

    print(f"=== {title} ===\n")
    print(f"Severity: {severity} (Scale: OK < INFO < WARN < CRITICAL)\n")

    raw_available = isinstance(raw, dict) and bool(raw)

    if summary_only:
        print_raw_hint(user_input, raw_available)
        return

    print_findings(findings)
    print_recommendations(recommendations)

    if show_raw:
        print_raw_evidence(raw)
    else:
        print_raw_hint(user_input, raw_available)


# -------------------------
# REQUEST HANDLING
# -------------------------

def send_request(
    payload,
    user_input,
    show_raw=False,
    summary_only=False,
    json_mode=False
):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)

    client.sendall(json.dumps(payload).encode())
    client.shutdown(socket.SHUT_WR)

    buffer = ""

    while True:
        chunk = client.recv(4096)
        if not chunk:
            break

        buffer += chunk.decode()

    client.close()

    try:
        response = json.loads(buffer)

        if json_mode:
            print(json.dumps(response, indent=2))
            return

        status = response.get("status")
        output = response.get("response")
        error = response.get("error")
        data = response.get("data", {})

        if status == "success":
            if isinstance(data, dict) and "severity" in data:
                format_argus_output(
                    output,
                    data,
                    user_input=user_input,
                    show_raw=show_raw,
                    summary_only=summary_only
                )
            else:
                print(output)

        elif status == "confirmation_required":
            print(output)

        elif status == "error":
            print(f"[ERROR] {error}")

        else:
            print(buffer)

    except json.JSONDecodeError:
        print(buffer, end="")


def is_pipe():
    return not sys.stdin.isatty()


def main():
    args = parse_args()

    if is_pipe():
        piped_input = sys.stdin.read()

        payload = {
            "data": {
                "input": piped_input
            },
            "mode": "pipe",
            "source": "cli_pipe",
            "stream": True,
            "trace": build_trace("cli_pipe")
        }

        send_request(
            payload,
            user_input="<piped input>",
            show_raw=args.raw,
            summary_only=args.summary,
            json_mode=args.json
        )
        return

    if not args.query:
        print('Usage: ai "your query"')
        return

    user_input = " ".join(args.query)

    payload = {
        "data": {
            "input": user_input
        },
        "mode": "cli",
        "source": "cli_direct",
        "stream": True,
        "trace": build_trace("cli_direct")
    }

    send_request(
        payload,
        user_input=user_input,
        show_raw=args.raw,
        summary_only=args.summary,
        json_mode=args.json
    )


if __name__ == "__main__":
    main()