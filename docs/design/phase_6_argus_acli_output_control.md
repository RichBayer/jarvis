# Phase 6 – Argus ACLI Output Control

---

## Purpose

Phase 6 begins the Distribution Layer work for Argus.

The goal of this phase is to improve user-facing output behavior without changing diagnostic logic, tool execution, or control-plane routing.

This phase focuses on:

- concise default output
- controlled raw evidence visibility
- summary-only display mode
- machine-readable JSON mode
- user-facing discoverability of raw evidence

This phase does not add new diagnostic intelligence.

---

## Scope

This work belongs to the CLI / ACLI presentation layer.

Initial implementation was performed in:

```text
scripts/ai_cli.py
```

Future distribution-specific implementation may move or extend this behavior into:

```text
distributions/argus/cli/acli.py
```

---

## Architectural Constraints

The output-control layer must not:

- bypass the daemon
- bypass the runtime manager
- bypass the control plane
- call system tools directly
- call Argus tools directly
- modify diagnostic logic
- modify structured tool output contracts
- remove or destroy raw evidence

All requests must continue to flow through:

```text
CLI
→ Daemon
→ Runtime Manager
→ Control Plane
→ Execution Engine
→ Argus Tool
→ System Tool
→ CommandRunner
→ OS
```

The CLI is responsible only for presentation behavior.

---

## Output Contract Preserved

Argus tools continue to return structured diagnostic data in the established format:

```text
{
  "severity": "...",
  "findings": [...],
  "recommendations": [...],
  "raw": { ... }
}
```

The CLI consumes this structured `data` field.

It must not parse formatted `message` output for diagnostic logic.

---

## Implemented Output Modes

### Default Mode

Example:

```bash
ai "disk"
```

Default mode now shows:

- title
- severity
- findings
- recommendations
- raw evidence hint

Raw evidence is hidden by default.

This reduces output noise while preserving diagnostic clarity.

---

### Raw Mode

Example:

```bash
ai --raw "disk"
```

Raw mode shows:

- title
- severity
- findings
- recommendations
- raw evidence

This preserves access to the original command evidence when the user wants to inspect it.

---

### Summary Mode

Example:

```bash
ai --summary "disk"
```

Summary mode shows:

- title
- severity
- raw evidence hint when raw evidence exists

This supports quick health checks without forcing the user to scan full diagnostic output.

---

### JSON Mode

Example:

```bash
ai --json "disk"
```

JSON mode prints the complete structured response from NeuroCore.

This preserves machine-readable workflows and verifies that the CLI presentation layer does not destroy underlying structured data.

---

## Raw Evidence Discoverability

Raw evidence is hidden by default, but the CLI now prints a copy/paste-ready hint when raw evidence is available.

Example:

```text
Raw evidence hidden by default.
To inspect raw evidence, run:
ai --raw "disk"
```

This avoids forcing users to memorize flags while keeping the default output concise.

---

## Validation Performed

The following commands were validated:

```bash
ai "disk"
ai --raw "disk"
ai --summary "disk"
ai --json "disk"
ai "memory"
ai "system"
```

Validation confirmed:

- default output is concise
- raw output remains available
- summary mode works
- JSON mode preserves structured response data
- the formatter works across multiple Argus commands
- multi-signal `system` output remains compatible

Syntax validation was also performed:

```bash
python -m py_compile scripts/ai_cli.py
```

---

## Screenshot Evidence

Screenshots were captured under:

```text
docs/screenshots/phase-6-output-control/
```

Captured evidence:

```text
01_disk_before_raw_output_default.png
02_disk_after_concise_default.png
03_disk_after_raw_flag_enabled.png
04_disk_after_raw_hint_added.png
05_disk_summary_mode.png
06_disk_json_mode.png
07_memory_concise_with_raw_hint.png
08_system_concise_with_raw_hint.png
```

---

## Deferred Ideas

During this work, additional usability ideas were identified but intentionally deferred.

Deferred items:

- deterministic friendly command aliases
- broader natural-language command routing
- model/router intent reasoning over fuzzy user phrasing
- interactive raw evidence prompts

These are not part of this implementation pass.

Reason:

The current phase must remain focused on output control and presentation behavior.

Routing changes belong in the control plane or future intelligence layers, not in the CLI formatter.

Interactive prompts may be considered later, but copy/paste raw evidence hints are safer for now because they preserve predictable CLI behavior for automation, piping, screenshots, and JSON workflows.

---

## Phase 6A Result

This pass establishes the first Phase 6 output-control behavior:

```text
Default output is concise.
Raw evidence is available on demand.
Summary and JSON modes are supported.
The CLI presentation layer remains separate from diagnostic logic.
```

This makes Argus easier to use without weakening the structured diagnostic contract established in Phase 5J.