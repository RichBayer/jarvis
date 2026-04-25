# Argus System Summary – Design (v1)

---

## Phase Alignment

Phase: 5J – Argus Tool Layer Expansion

This implementation establishes the **first fully compliant Argus diagnostic tool**.

---

## Purpose

Transform `system_summary` from a placeholder into a **deterministic system diagnostic tool**.

This tool will:

- consume raw system tool data
- interpret system state
- produce structured findings
- establish the Argus tool pattern

---

## Architectural Role

Layer: Argus Tool Layer

Responsibilities:

- interpret system tool data
- generate findings
- assign severity
- produce recommendations

Constraints:

- MUST NOT call CommandRunner
- MUST use system tools only
- MUST consume structured `data`
- MUST NOT parse CLI `message`

---

## Input

Source tool:

system_info (target="system")

Data structure:

```
{
  "hostname": { "raw": {...} },
  "uptime": { "raw": {...} },
  "os": { "raw": {...} },
  "cpu": { "raw": {...} },
  "memory": { "raw": {...} },
  "disk": { "raw": {...} }
}
```

---

## Output Contract

```
{
  "status": "success",
  "message": "System Summary [SEVERITY]",
  "data": {
    "severity": "OK | INFO | WARN | CRITICAL",
    "findings": [
      {
        "severity": "...",
        "component": "...",
        "message": "...",
        "evidence": { ... }
      }
    ],
    "recommendations": [
      "..."
    ]
  }
}
```

---

## Severity Model

Levels:

- OK → no issues
- INFO → informational signal
- WARN → potential issue
- CRITICAL → immediate concern

Severity escalates based on highest finding.

---

## Interpretation Strategy

Initial version focuses on:

### 1. Command Success Validation
- Ensure return codes = 0
- Detect execution failures

### 2. Data Presence Validation
- Ensure expected fields exist
- Detect missing outputs

### 3. Basic Signal Extraction (Phase 1)
- uptime string presence
- memory output presence
- disk output presence

NOTE:
Deep parsing (percentages, thresholds) is deferred to next iteration.

---

## Findings Structure

Each finding must include:

- severity
- component (cpu, memory, disk, etc.)
- message
- evidence (raw snippet or metadata)

---

## Recommendations

Rules:

- Only added when severity ≥ WARN
- Must be actionable
- Must map to findings

---

## Observability

Must emit:

- argus_tool_invoked
- argus_summary_completed

Must preserve:

- trace context
- request_id continuity

---

## Future Expansion (NOT in this build)

- numeric parsing (CPU %, memory %)
- threshold-based severity
- anomaly detection
- incident memory integration

---

## Success Criteria

- consumes ONLY structured data
- produces deterministic findings
- follows output contract
- does NOT parse message field
- establishes reusable Argus pattern

---

## Notes

This is the **reference implementation** for all future Argus tools.
Implementation complete — validated against live system execution and CLI output.