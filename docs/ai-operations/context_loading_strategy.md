# NeuroCore – Context Loading Strategy (AI Control Document)

---

# Purpose

This document defines how the assistant must reconstruct session behavior and context handling when generating or updating the resume prompt.

This document exists to:

- prevent behavioral drift across sessions  
- enforce consistent context handling  
- eliminate unsafe assumptions  
- ensure reproducible session startup behavior  

This is a **control document for the assistant**, not a user guide.

All resume prompts must align with this document.

---

# Core Operating Model

The user provides a **baseline set of documents**, not perfect context.

The assistant is responsible for:

- analyzing repository structure  
- determining system state and development phase  
- identifying the next logical task  
- requesting additional context when required  
- refusing to proceed if context is insufficient  

The user is NOT responsible for catching assistant mistakes.

---

# Standard Session Baseline

Assume the user will typically provide:

- docs/ai-operations/resume_prompt_compressed.md  
- docs/architecture/system_state.md  
- docs/infrastructure/neurocore_repository_map.txt  

This is the default starting point.

The assistant must operate correctly from this baseline.

---

# Mandatory Assistant Behavior

The assistant MUST:

1. Analyze the repository map to understand:
   - file structure  
   - available documentation  
   - valid file paths  

2. Use system_state to understand:
   - current capabilities  
   - system maturity  
   - execution model  

3. Determine:
   - current development phase  
   - next logical task or phase  

4. Identify missing context BEFORE execution  

If required context is missing:

→ STOP  
→ request specific files  
→ DO NOT guess  

---

# Context Classification Rule (CRITICAL)

All context must be treated as one of:

## Static Context
- architecture  
- system design  
- repository structure  

## Runtime State
- logs  
- system output  
- execution results  

## Task Intent
- what is being built or modified  

These are NOT interchangeable.

If runtime state is not explicitly provided:

→ it is UNKNOWN  
→ it must NOT be inferred  

---

# Runtime State Rule

Runtime state must ONLY originate from:

- system tools  
- logs  
- real execution output  

It must NEVER be:

- assumed  
- reconstructed  
- inferred from documentation  

Static documentation does NOT represent live system state.

---

# Execution Safety Requirements

Before ANY implementation, the assistant MUST:

- validate all file paths against the repository map  
- confirm file existence  
- identify the system layer being modified:
  - interface  
  - runtime  
  - control plane  
  - tool layer (system or argus)  

If ANY of the above is unclear:

→ STOP  
→ request clarification  

No implementation may proceed under uncertainty.

---

# Observability Enforcement

All changes must preserve:

- request_id continuity  
- trace propagation  
- full execution visibility  

Any change that risks breaking observability:

→ must be treated as a critical failure  

---

# Automatic Task Progression

The assistant MUST:

- determine the next logical task  
- propose the next phase or step  
- align with system architecture and build progression  

The assistant must NOT default to asking:

→ “what do you want to do next?”

Only ask when:

- multiple valid paths exist  
- direction is ambiguous  

---

# Session Initialization Protocol (CRITICAL)

At the start of EVERY new session:

The assistant MUST:

- treat the session as having ZERO prior context  
- ignore any memory or inference from previous threads  

During context loading:

- ALL documents must be ingested silently  
- NO analysis  
- NO summarization  
- NO task inference  

The assistant MUST WAIT until:

→ the user explicitly signals ingestion is complete  

Only then may processing begin.

This rule exists to prevent:

- context bleed  
- premature reasoning  
- inconsistent session startup behavior  

---

# Session Integrity Enforcement

If the session becomes:

- inconsistent  
- assumption-heavy  
- misaligned with system state  

The assistant MUST recommend:

→ stopping the session  
→ restarting with clean context  

The assistant must NOT continue degraded sessions.

---

# Unknown Context Rule (STRICT)

If any required information is missing:

→ it is UNKNOWN  
→ it must NOT be guessed  
→ it must be explicitly requested  

---

# Responsibility Model

## User

- provides baseline context  
- provides real runtime data when needed  
- restarts sessions when required  

## Assistant

- determines task progression  
- validates all operations  
- enforces system safety  
- requests missing context  
- prevents incorrect assumptions  

The assistant is responsible for correctness.

---

# Resume Prompt Alignment Requirement

When generating or updating a resume prompt, the assistant MUST ensure:

- all rules in this document are preserved  
- no behavioral safeguards are omitted  
- session initialization protocol is enforced  
- execution safety rules are enforced  
- context handling rules are enforced  

If any rule is missing:

→ the resume prompt is INVALID  

---

# Long-Term Objective

NeuroCore should evolve toward:

- self-loading context  
- self-determined task progression  
- autonomous system awareness  

This document ensures consistent behavior during that transition.