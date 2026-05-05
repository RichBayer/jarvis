# NeuroCore / Argus – Phase-Aware Documentation & Development Integration

---

## Purpose

This document defines WHEN and HOW system components must be implemented relative to development phases.

It exists to:

- prevent premature implementation
- avoid architectural rework
- ensure correct build sequencing
- align documentation with actual system state

This is a CONTROL document.

All development and documentation must follow this progression.

---

## Core Principle

NeuroCore is built in layers.

Argus depends on those layers.

Therefore:

Features must ONLY be implemented when their required foundation exists.

---

## System Layer Dependency Model

The system is built in this order:

1. Runtime (daemon, control plane, execution engine)
2. System Tool Layer (data collection)
3. Argus Tool Layer (interpretation)
4. Distribution Layer (ACLI)
5. Intelligence Enhancements (model, memory, training)

Each layer depends on the one before it.

---

## Current Development Position

System is currently in:

## Phase 6 – Distribution Layer (CURRENT)

Phase 5J is COMPLETE.

Phase 5J should be considered complete only after the raw-evidence contract closeout documented in:

build-logs/025_system_analysis_multi_signal.md

Phase 6A first output-control pass is COMPLETE.

Phase 6A output-control behavior is documented in:

build-logs/026_phase_6_argus_acli_output_control.md  
docs/design/phase_6_argus_acli_output_control.md  

Phase 6 output-control continuation is COMPLETE.

Documented in:

build-logs/027_phase_6_argus_acli_completion.md  
docs/design/phase_6_argus_acli_output_control.md  
docs/design/argus_acli_user_experience_layer.md  
docs/distributions/argus/acli_spec.md  

Confirmed capabilities:

- execution engine COMPLETE
- control plane COMPLETE
- system tools ACTIVE
- structured data model FULLY ENFORCED across all system tools
- Argus diagnostic layer FULLY IMPLEMENTED across implemented core domains
- deterministic interpretation ACTIVE (severity + findings + recommendations)
- raw evidence preservation ACTIVE across implemented Argus diagnostic tools
- multi-signal system aggregation ACTIVE through system_analysis
- structured CLI diagnostic output ACTIVE
- Phase 6 concise default Argus output ACTIVE
- Phase 6 raw evidence mode ACTIVE through --raw
- Phase 6 summary mode ACTIVE through --summary
- Phase 6 JSON mode ACTIVE through --json
- Phase 6 copy/paste raw evidence hints ACTIVE
- Phase 6 severity filtering ACTIVE through --severity
- Phase 6 signal filtering ACTIVE through --signal
- Argus-facing acli command path ACTIVE

---

## Phase-Based Implementation Rules

---

### Phase 5J (COMPLETE) – Argus Tool Layer

This phase is COMPLETE and serves as a foundational reference.

What was achieved:

- full Argus diagnostic layer across implemented system domains  
- structured output contract enforced across ALL system tools  
- deterministic interpretation pattern established  
- consistent tool composition model (system → Argus)  
- stable control plane routing for diagnostic commands  
- raw evidence preservation across implemented Argus diagnostic tools  
- multi-signal system aggregation through system_analysis  

Established pattern:

system tool → structured data → interpretation → normalized output → raw evidence

This pattern is now canonical and must be followed for all future Argus development.

---

### MUST have been implemented DURING Phase 5J

(These are now COMPLETE and must be preserved)

#### 1. Structured Output Contract

All tools return:

- message (human-readable)
- data (machine-readable)

Argus tools include:

- severity
- findings
- recommendations
- raw evidence

Status: COMPLETE

---

#### 2. System Tool Data Compliance

ALL system tools:

- return structured data
- do NOT rely on raw text output
- preserve raw command output for downstream use

Status: COMPLETE

---

#### 3. Argus Tool Pattern Enforcement

ALL implemented Argus tools:

- consume system tool data
- produce structured findings
- remain deterministic
- preserve raw evidence for verification

Status: COMPLETE

---

#### 4. Command Consistency (Control Plane)

Command patterns stabilized:

summary  
processes  
disk  
memory  
logs  
network  
connections  
uptime  
system  

Status: STABLE

---

#### 5. Incident Memory Integration Points

Defined but NOT implemented:

- incident candidate structure
- generation point (Argus tools)
- deterministic signature approach

Status: DEFINED ONLY

---

### MUST NOT be implemented in Phase 5J

- full installer
- packaging (deb, rpm, etc.)
- multi-distro abstraction
- advanced model integration
- training system (Argus Lab)
- evaluation systems
- automation / remediation

---

## Phase 6 – Distribution Layer (CURRENT)

This is where Argus becomes a real user-facing product.

---

### To be implemented in Phase 6

#### 1. Argus ACLI User Experience Layer (PRIMARY FOCUS)

Create:

distributions/argus/cli/acli.py

Goals:

- improve CLI output readability  
- structure findings clearly  
- group results by severity  
- refine human-readable summaries  
- introduce filtering  
- introduce summarization  
- allow signal selection  
- control raw output visibility  
- make outputs feel like a real tool, not raw data  

Constraints:

- MUST NOT bypass control plane  
- MUST preserve structured output contract  
- MUST preserve access to raw evidence  
- MUST consume Argus tool outputs (not system tools directly)
- MUST NOT move diagnostic interpretation into the CLI/distribution layer

---

#### Phase 6A Output-Control Pass

Status: COMPLETE

Implemented in:

scripts/ai_cli.py

Completed behavior:

- concise default Argus diagnostic output
- on-demand raw evidence display through --raw
- summary-only output through --summary
- full structured response output through --json
- copy/paste raw evidence hints

---

#### Phase 6 Output-Control Completion Pass

Status: COMPLETE

Implemented in:

scripts/ai_cli.py

Completed behavior:

- report-style diagnostic formatting
- severity-sorted findings
- component/severity finding labels
- display-only severity filtering through --severity
- display-only signal filtering through --signal
- combined signal + severity filtering
- filtered recommendation labeling
- command-name-aware behavior (ai vs acli)
- Argus-facing acli command available via symlink
- target-first command ergonomics (acli system --signal disk)

Remaining Phase 6 distribution-layer work may include:

- improved multi-signal formatting if needed
- production vs training output profiles
- eventual move or mirror into distributions/argus/cli/acli.py
- runtime packaging planning
- filesystem layout planning

---

#### 2. Runtime Packaging (INITIAL, NOT FINAL)

Bundle runtime, tools, and Argus tools with minimal friction.

---

#### 3. File System Layout (PLANNING LEVEL)

Example:

/opt/argus/  
/opt/argus/runtime/  
/opt/argus/tools/  

User data:

~/.argus/

---

#### 4. Incident Memory (PHASE-ALIGNED FUTURE WORK)

May be implemented later if aligned with current work.

---

## Phase 7 – Intelligence Layer

Model integration and reasoning enhancements.

---

## Phase 8 – Training System (Argus Lab)

Scenario-driven training environment.

---

## Documentation Integration Rules

Phase 5J docs → architecture/ or design/  
Distribution docs → distributions/argus/  
Contracts → architecture/  
Vision → vision/

---

## Validation Rule

Before implementing ANY feature:

1. Does the required lower layer exist?
2. Is structured data available?
3. Does this violate current phase boundaries?

If any answer is no → STOP

---

## Final Principle

Build in order.

Do NOT:

- skip layers
- mix responsibilities
- introduce future features early

---

## End State Goal

A system that:

- gathers real system data
- interprets it deterministically
- preserves supporting evidence
- optionally enhances it with AI
- evolves into a full training and intelligence platform