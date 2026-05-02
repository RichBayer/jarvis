# Argus ACLI User Experience Layer – Design

---

## Objective

Transform Argus output from raw diagnostic data into a clean, structured, user-friendly CLI experience.

The system already produces correct diagnostics.

This phase focuses on:

- presentation
- readability
- usability
- consistency

NOT new system intelligence.

---

## Scope

This phase operates at the **Distribution Layer (Argus ACLI)**.

It MUST NOT:

- modify system tools
- modify Argus diagnostic logic
- bypass the control plane
- introduce new execution paths

It ONLY transforms how results are presented to the user.

---

## Current State

Argus tools return structured output:

```
{
  "status": "success",
  "tool": "<name>",
  "message": "...",
  "data": {
    "severity": "...",
    "findings": [...],
    "recommendations": [...],
    "raw": { ... }
  }
}
```

The current CLI already presents:

- title / summary
- severity
- findings
- recommendations
- raw evidence

This is correct and contract-aligned.

The next problem is not whether the data exists.

The next problem is controlling how much of it is shown by default.

---

## Implementation Status

The first Phase 6 output-control pass is complete.

Documented in:

```text
docs/design/phase_6_argus_acli_output_control.md
build-logs/026_phase_6_argus_acli_output_control.md
```

Implemented in:

```text
scripts/ai_cli.py
```

Completed behavior:

- concise default Argus diagnostic output
- on-demand raw evidence display with `--raw`
- summary-only output with `--summary`
- full structured response output with `--json`
- copy/paste raw evidence hint when raw evidence exists

Remaining Phase 6 work may still include:

- selected-signal output controls
- severity/filtering modes
- improved multi-signal formatting
- production vs training output profiles
- eventual move or mirror of finalized behavior into `distributions/argus/cli/acli.py`

---

## Problem

Current CLI output:

- can become noisy as raw evidence grows
- mixes interpreted findings and raw evidence in one long output
- lacks output modes for different user needs
- does not yet support summary-only views
- does not yet support raw-output toggles
- does not yet support signal selection
- is harder to scan quickly during repeated diagnostic workflows

The system now has the evidence it needs.

Phase 6 focuses on making that evidence usable without overwhelming the user.

---

## Design Goals

### 1. Readability

Output must be:

- easy to scan
- clearly segmented
- visually structured

---

### 2. Severity Awareness

Severity must be:

- immediately visible
- consistently formatted

Example:

[OK]  
[INFO]  
[WARN]  
[CRITICAL]

---

### 3. Structured Sections

Each output should follow:

1. Title / Summary
2. Severity
3. Findings
4. Recommendations
5. Raw Evidence (optional or controlled by output mode)

---

### 4. Consistency

All Argus outputs must:

- follow the same structure
- use the same formatting rules
- feel like a unified tool

---

### 5. No Data Loss

All structured data must still exist.

This layer:

- formats
- filters display
- controls visibility
- does NOT remove or alter underlying diagnostic data

---

## Proposed Output Format

Default concise example:

```
=== Disk Analysis ===

Severity: WARN

Findings:
- High disk usage on /mnt/c (77%)

Recommendations:
- Investigate disk usage
- Free up space
```

Verbose / raw-enabled example:

```
=== Disk Analysis ===

Severity: WARN

Findings:
- High disk usage on /mnt/c (77%)

Recommendations:
- Investigate disk usage
- Free up space

--- RAW OUTPUT ---

[DISK_USAGE]
Filesystem      Size  Used Avail Use% Mounted on
...
```

---

## Implementation Approach

### Option A – CLI / ACLI Formatting Layer (Preferred)

Modify or extend the interface layer:

```
scripts/ai_cli.py
```

and later:

```
distributions/argus/cli/acli.py
```

Responsibilities:

- detect Argus output
- format structured diagnostic data for display
- support output modes
- control raw evidence visibility
- preserve raw JSON / structured data internally

Possible output modes:

- default concise output
- verbose output with raw evidence
- summary-only output
- filtered severity output
- selected-signal output

---

### Option B – Argus Presentation Wrapper (Alternative)

Introduce formatting layer inside Argus tools.

NOT preferred because:

- mixes logic and presentation
- breaks separation of concerns
- makes future output modes harder to manage

---

## Decision

Use:

→ CLI / ACLI Formatting Layer

Argus tools remain responsible for:

- interpretation
- severity
- findings
- recommendations
- raw evidence preservation

The interface/distribution layer is responsible for:

- presentation
- filtering
- summarization
- raw visibility control
- user-facing output behavior

---

## Key Constraints

- MUST preserve control plane execution flow
- MUST NOT modify tool output contract
- MUST NOT parse `message` field for logic
- MUST rely on structured `data` field
- MUST preserve access to raw evidence
- MUST NOT move diagnostic interpretation into the CLI / ACLI layer
- MUST NOT hide data permanently; filtering is display-only

---

## Future Extensions

- colorized output
- table formatting
- interactive CLI
- filtering options (e.g. show only WARN/CRITICAL)
- summary-only mode
- verbose/raw mode
- signal selection (e.g. disk only, network only, processes only)
- machine-readable output mode
- profile-based output behavior for production vs training personalities

---

## Summary

This phase converts:

structured diagnostic output with raw evidence  
→ into  
a controlled, usable system interface

No new intelligence is added.

Only clarity, control, and usability.

---

## End State

A user can run:

```
ai "disk"
```

or later:

```
argus disk
```

And instantly understand:

- system health
- problems
- what to do next
- whether raw evidence is needed

Without being forced to read every raw command output by default.