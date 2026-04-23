# NeuroCore – Mid-Phase Reset Protocol (AI Control Document)

## Purpose

This document defines the **mandatory checkpoint and reset procedure** when a build phase is NOT complete but the session must be restarted.

This protocol exists to:

- prevent loss of in-progress work
- eliminate ambiguity when resuming development
- preserve accurate system state during interruptions
- prevent drift caused by long or degraded sessions
- ensure resume prompt reflects REAL build position

This is a **control document for the assistant**, not a user guide.

---

## Core Principle

**Incomplete work must be documented as incomplete — never inferred as complete.**

At no point may the assistant:

- assume completion
- imply stability
- present partial work as finalized

---

## When This Protocol Is Triggered

This protocol MUST be executed when:

- the session becomes long or degraded
- context accuracy is uncertain
- the assistant detects drift or inconsistency
- the user requests a reset or new thread
- documentation cannot be safely completed in current session

This protocol MUST be executed BEFORE starting a new thread.

---

## 🚨 RESET PREVENTION RULE (CRITICAL)

The assistant MUST NOT allow a session reset without checkpointing.

If the user attempts to reset without checkpointing:

→ STOP  
→ initiate Mid-Phase Reset Protocol  

---

## Context Integrity Trigger

If the assistant determines:

- context may be stale
- documents may no longer be reliable
- prior uploaded context is no longer available

→ the session MUST be reset  
→ but ONLY AFTER checkpointing is complete  

---

## Checkpoint Scope

This protocol captures **partial system state**, NOT final documentation.

Required outputs:

- Partial Build Log (REQUIRED)
- Design Document Update (REQUIRED)
- Resume Prompt Update (CRITICAL)

Optional (ONLY if impacted):

- system_state.md

Full documentation sweep is NOT performed here.

---

## State Classification (MANDATORY)

The assistant MUST classify all work into:

### Completed Work
Fully implemented and verified components

### In-Progress Work
Partially implemented components

### Not Started Work
Planned but untouched components

This classification MUST be explicit.

---

## Partial Build Log (REQUIRED)

Location:

/mnt/g/ai/projects/neurocore/build-logs/

### Naming Convention

Continue current phase log OR create new entry if needed.

### Required Label

The build log MUST clearly state:

> **⚠️ INCOMPLETE PHASE CHECKPOINT**

---

### Build Log Structure (Checkpoint Version)

1. Starting State
2. Intended Objective of Phase
3. Work Completed So Far
4. Work In Progress
5. Known Issues / Broken State (if any)
6. Remaining Work
7. Next Immediate Step (CRITICAL)

---

### Build Log Rules

The build log MUST:

- reflect REAL work only
- NOT fabricate progress
- NOT imply completion
- accurately describe system condition (even if broken)
- include screenshots if available (optional)

---

## Design Document Update (REQUIRED)

Location:

/mnt/g/ai/projects/neurocore/docs/design/<feature>.md

The assistant MUST update the design doc to reflect:

- current implementation state
- deviations from original design (if any)
- incomplete sections clearly marked

---

## Resume Prompt Update (CRITICAL)

The assistant MUST update:

docs/ai-operations/resume_prompt_compressed.md

---

### Sections That MUST Be Updated

```
🎯 CURRENT PHASE (VALIDATE)
🎯 CURRENT FOCUS (VALIDATE)
🎯 NEXT TASKS (VALIDATE)
```

---

### Resume Prompt Rules

The assistant MUST:

- reflect actual current state (NOT planned state)
- reflect incomplete work accurately
- define EXACT next step

---

### Next Task Precision Rule (CRITICAL)

Next tasks MUST be:

- concrete
- actionable
- implementation-level

NOT allowed:

- vague continuation instructions
- high-level summaries

---

## Example (Conceptual)

BAD:
"Continue building Argus tools"

GOOD:
"Implement data aggregation logic inside tools/argus/process_top.py using output from process_top system tool"

---

## System State Update (CONDITIONAL)

Only update:

docs/architecture/system_state.md

IF:

- system behavior has materially changed
- new capabilities exist (even partial)

DO NOT update for:

- incomplete or unstable work
- purely structural scaffolding

---

## Repository Validation Rule

Before writing ANY file:

The assistant MUST:

- validate file paths using repository map
- confirm existence of files

The assistant MUST NOT:

- invent paths
- assume files exist

---

## Output Format Requirements

The assistant MUST provide:

1. List of files being updated
2. Reason for each update
3. FULL file replacements

All files MUST:

- be in individual code blocks
- use four backticks (````)

---

## Post-Checkpoint Instructions (MANDATORY)

After checkpointing, the assistant MUST instruct the user to:

### Start a New Session

Upload:

- docs/ai-operations/resume_prompt_compressed.md
- docs/ai-operations/context_loading_strategy.md
- docs/infrastructure/neurocore_repository_map.txt
- docs/architecture/system_state.md (if applicable)
- Design document for current feature (RECOMMENDED)

---

## Session Restart Goal

The next session MUST:

- resume exactly where the checkpoint left off
- require ZERO guessing
- continue from validated system state

---

## Final Rule

If a session must be reset:

→ checkpoint FIRST  
→ reset SECOND  

Failure to checkpoint results in:

- lost work
- inconsistent system state
- documentation drift

This