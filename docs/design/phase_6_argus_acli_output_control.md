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
- improved readability and report-style formatting
- display-only filtering controls (severity + signal)
- shaping the actual ACLI user experience

This phase does not add new diagnostic intelligence.

---

## Scope

This work belongs to the CLI / ACLI presentation layer.

Initial implementation was performed in:

scripts/ai_cli.py

Future distribution-specific implementation may move or extend this behavior into:

distributions/argus/cli/acli.py

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

CLI → Daemon → Runtime Manager → Control Plane → Execution Engine → Argus Tool → System Tool → CommandRunner → OS

The CLI is responsible only for presentation behavior.

---

## Output Contract Preserved

Argus tools continue to return structured diagnostic data in the established format:

{
  "severity": "...",
  "findings": [...],
  "recommendations": [...],
  "raw": { ... }
}

The CLI consumes this structured data field.

It must not parse formatted message output for diagnostic logic.

---

## Implemented Output Modes

### Default Mode

Example:

ai "disk"

Default mode now shows:

- title
- severity
- findings
- recommendations
- raw evidence hint

Additional improvements:

- findings are sorted by severity
- findings include structured labels: [component] [severity]
- output uses report-style spacing and indentation

Raw evidence is hidden by default.

---

### Raw Mode

Example:

ai --raw "disk"

Raw mode shows:

- title
- severity
- findings
- recommendations
- raw evidence

---

### Summary Mode

Example:

ai --summary "disk"

Summary mode shows:

- title
- severity
- raw evidence hint when raw evidence exists

---

### JSON Mode

Example:

ai --json "disk"

JSON mode prints the complete structured response from NeuroCore.

This remains unfiltered and untouched.

---

## Additional Output Controls (Build 027)

### Severity Filtering (Display Only)

Example:

ai --severity WARN "system"

- filters displayed findings by minimum severity
- does NOT modify:
  - underlying data
  - recommendations
  - raw evidence
  - JSON output

---

### Signal Filtering (Display Only)

Example:

ai --signal disk "system"

- filters findings by component
- uses structured component field
- works with multi-signal outputs

---

### Combined Filtering

Example:

ai --signal disk --severity WARN "system"

- allows precise filtering of displayed results
- underlying diagnostic data remains unchanged

---

### Recommendation Labeling

When filters are active, output now shows:

Recommendations from full diagnostic:

This avoids implying that recommendations were filtered along with findings.

---

### Command Name Awareness

The CLI adapts based on how it is invoked:

ai "system"  
acli "system"

- raw evidence hints use the active command name
- CLI usage reflects the invoked command

---

### ACLI Command Availability

ACLI is now available as a command:

/usr/local/bin/acli -> scripts/ai_cli.py

This introduces the Argus-facing command without requiring a separate implementation yet.

---

## Raw Evidence Discoverability

Raw evidence is hidden by default, but the CLI prints a copy/paste-ready hint.

Example:

Raw evidence hidden by default.  
To inspect raw evidence, run:  
ai --raw "disk"

---

## Validation Performed

The following commands were validated:

ai "disk"  
ai --raw "disk"  
ai --summary "disk"  
ai --json "disk"  
ai "memory"  
ai "system"  

ai --severity WARN "system"  
ai --severity CRITICAL "system"  
ai --signal disk "system"  
ai --signal network "system"  
ai --signal disk --severity WARN "system"  

acli system  
acli disk  
acli memory  
acli network  
acli logs  

Validation confirmed:

- formatting works across all domains
- filtering behaves correctly (including empty cases)
- JSON output remains unmodified
- raw evidence remains accessible
- CLI behavior is consistent across ai and acli

Syntax validation:

python -m py_compile scripts/ai_cli.py

---

## Screenshot Evidence

Screenshots were captured under:

docs/screenshots/phase-6-acli-completion/

Captured evidence includes:

- baseline output modes
- formatting improvements
- severity filtering behavior
- signal filtering behavior
- combined filtering
- recommendation labeling behavior
- ai vs acli command differences

---

## ACLI UX Direction (Clarified)

This phase clarified how ACLI should feel to use.

ACLI is not:

- just a command tool
- or just a natural-language interface

It must support both.

---

### Natural / Fuzzy Mode (Primary UX Direction)

acli "what's wrong with my system?"  
acli "why is disk warning?"  
acli "what should I check next?"

---

### Direct Command Mode

acli system  
acli disk  
acli memory  
acli network  

---

### Power User Mode

acli system --signal disk  
acli system --severity WARN  
acli --raw system  
acli --json system  

---

### Key Principle

ACLI should feel simple first, but remain extremely powerful when needed.

---

### Important Constraint

Natural-language routing must NOT be implemented in the CLI.

It belongs in:

router → reasoning → control plane

The CLI remains a clean interface layer.

---

## Deferred Ideas

Deferred items:

- broad natural-language routing
- router-based intent interpretation
- pasted-output reasoning
- interactive workflows
- production vs training output profiles

These are intentionally not implemented here.

---

## Phase 6 Result

Phase 6 now establishes:

Readable, structured output  
Controlled visibility of raw evidence  
Multiple output modes (default, raw, summary, JSON)  
Display-only filtering (severity + signal)  
Clear separation between presentation and logic  
A defined ACLI user experience direction  

This makes Argus significantly more usable without changing the underlying system design.