#!/usr/bin/env python3

import sys
import json
import socket
import uuid
import argparse
from pathlib import Path

SOCKET_PATH = "/tmp/neurocore.sock"

SEVERITY_ORDER = {
    "CRITICAL": 0,
    "WARN": 1,
    "INFO": 2,
    "OK": 3,
    "UNKNOWN": 4
}


def command_name():
    return Path(sys.argv[0]).name or "ai"


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
        prog=command_name(),
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

    parser.add_argument(
        "--severity",
        choices=["CRITICAL", "WARN", "INFO", "OK", "UNKNOWN"],
        help="Only display findings at this severity or higher"
    )

    parser.add_argument(
        "--signal",
        help="Only display findings for this signal/component"
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


def severity_rank(severity):
    return SEVERITY_ORDER.get(str(severity).upper(), SEVERITY_ORDER["UNKNOWN"])


def sorted_findings(findings):
    return sorted(
        findings,
        key=lambda finding: severity_rank(finding.get("severity"))
        if isinstance(finding, dict)
        else severity_rank("UNKNOWN")
    )


def finding_matches_severity(finding, minimum_severity):
    if not minimum_severity:
        return True

    if not isinstance(finding, dict):
        return True

    minimum_rank = severity_rank(minimum_severity)
    finding_rank = severity_rank(finding.get("severity"))

    return finding_rank <= minimum_rank


def finding_matches_signal(finding, signal_filter):
    if not signal_filter:
        return True

    if not isinstance(finding, dict):
        return False

    component = finding.get("component")

    if not component:
        return False

    return str(component).lower() == str(signal_filter).lower()


def filter_findings(findings, minimum_severity=None, signal_filter=None):
    filtered_findings = []

    for finding in findings:
        if not finding_matches_severity(finding, minimum_severity):
            continue

        if not finding_matches_signal(finding, signal_filter):
            continue

        filtered_findings.append(finding)

    return filtered_findings


def format_finding(finding):
    if isinstance(finding, dict):
        message = finding.get("message", str(finding))
        severity = finding.get("severity")
        component = finding.get("component")

        label_parts = []

        if component:
            label_parts.append(str(component))

        if severity:
            label_parts.append(str(severity))

        if label_parts:
            label = " ".join(f"[{part}]" for part in label_parts)
            return f"  - {label} {message}"

        return f"  - {message}"

    return f"  - {str(finding)}"


def no_findings_message(minimum_severity=None, signal_filter=None):
    if minimum_severity and signal_filter:
        return (
            f"  - None for signal {signal_filter} "
            f"at severity {minimum_severity} or higher"
        )

    if minimum_severity:
        return f"  - None at severity {minimum_severity} or higher"

    if signal_filter:
        return f"  - None for signal {signal_filter}"

    return "  - None"


def print_findings(findings, minimum_severity=None, signal_filter=None):
    filtered_findings = filter_findings(
        findings,
        minimum_severity=minimum_severity,
        signal_filter=signal_filter
    )

    if not filtered_findings:
        print("Findings:")
        print(no_findings_message(
            minimum_severity=minimum_severity,
            signal_filter=signal_filter
        ))
        print()
        return

    print("Findings:")

    formatted_findings = [
        format_finding(finding)
        for finding in sorted_findings(filtered_findings)
    ]

    print("\n\n".join(formatted_findings))
    print()


def print_recommendations(
    recommendations,
    filtered_view=False
):
    if filtered_view:
        print("Recommendations from full diagnostic:")
    else:
        print("Recommendations:")

    if recommendations:
        formatted_recommendations = [
            f"  - {recommendation}"
            for recommendation in recommendations
        ]

        print("\n\n".join(formatted_recommendations))
    else:
        print("  - None")

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
    print()
    print(
        f'  - To inspect raw evidence, run: '
        f'{command_name()} --raw "{user_input}"'
    )


def format_argus_output(
    output,
    data,
    user_input,
    show_raw=False,
    summary_only=False,
    minimum_severity=None,
    signal_filter=None
):
    severity = data.get("severity", "UNKNOWN")
    findings = data.get("findings", [])
    recommendations = data.get("recommendations", [])
    raw = data.get("raw", {})

    title = clean_title(output)

    print()
    print(f"=== {title} ===\n")
    print(f"Severity: {severity} (Scale: OK < INFO < WARN < CRITICAL)\n")

    raw_available = isinstance(raw, dict) and bool(raw)
    filtered_view = bool(minimum_severity or signal_filter)

    if summary_only:
        print_raw_hint(user_input, raw_available)
        print()
        return

    print_findings(
        findings,
        minimum_severity=minimum_severity,
        signal_filter=signal_filter
    )
    print_recommendations(
        recommendations,
        filtered_view=filtered_view
    )

    if show_raw:
        print_raw_evidence(raw)
        print()
    else:
        print_raw_hint(user_input, raw_available)
        print()


# -------------------------
# REQUEST HANDLING
# -------------------------

def send_request(
    payload,
    user_input,
    show_raw=False,
    summary_only=False,
    json_mode=False,
    minimum_severity=None,
    signal_filter=None
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
                    summary_only=summary_only,
                    minimum_severity=minimum_severity,
                    signal_filter=signal_filter
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
            json_mode=args.json,
            minimum_severity=args.severity,
            signal_filter=args.signal
        )
        return

    if not args.query:
        print(f'Usage: {command_name()} "your query"')
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
        json_mode=args.json,
        minimum_severity=args.severity,
        signal_filter=args.signal
    )


if __name__ == "__main__":
    main()