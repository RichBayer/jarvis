# NeuroCore – Documentation Closeout Protocol (AI Control Document)

## Purpose

This document defines the **mandatory documentation workflow** that must be executed at the end of every completed build phase.

This document exists to:

- enforce consistent documentation across all build phases
- eliminate documentation drift
- ensure system documentation reflects actual implementation
- standardize build log structure and quality
- guarantee all affected documentation is updated before phase completion

This is a **control document for the assistant**, not a user guide.

All documentation actions must comply with this protocol.

---

## Core Principle

**Documentation must reflect reality — not intention.**

If implementation and documentation conflict:

→ documentation MUST be updated to match implementation

---

## When This Protocol Is Triggered

This protocol MUST be executed:

- at the end of any completed build phase
- before committing changes
- before pushing to the repository
- when explicitly requested by the user

This protocol MUST NOT be skipped.

---

## 🚨 CONTEXT INTEGRITY CHECK (PRE-CLOSEOUT GATE)

Before performing ANY documentation work, the assistant MUST verify that valid context is loaded.

The assistant MUST confirm access to:

- docs/ai-operations/resume_prompt_compressed.md
- docs/ai-operations/context_loading_strategy.md
- docs/infrastructure/neurocore_repository_map.txt
- docs/architecture/system_state.md (if required)

If ANY of the above are:

- missing
- outdated
- uncertain
- or were loaded earlier in a long or degraded session

→ STOP  
→ request re-upload of required documents  
→ DO NOT proceed with documentation  

Documentation MUST NOT be performed under uncertain context conditions.

---

## Documentation Responsibility Model

User:

- provides baseline context (if requested)
- confirms when build phase is complete

Assistant:

- determines all documentation impacted by the build phase
- updates ALL affected documentation
- ensures documentation consistency across the system
- enforces all documentation rules in this protocol

The assistant is responsible for documentation completeness and correctness.

---

## Documentation Sweep (MANDATORY ORDER)

The assistant MUST review documentation in the following order:

1. Build Log (REQUIRED)
2. System State
3. Architecture Documentation
4. Design Documentation
5. Tool Manifests / Specifications
6. Repository Map (if structure changed)
7. System Map (if environment changed)
8. Documentation Index / README (if navigation changed)

This order MUST be followed.

---

## Impact Detection Rule (CRITICAL)

The assistant MUST determine which documents were affected by the completed build phase.

The assistant MUST NOT wait for the user to specify which documents to update.

If a document is impacted:

→ it MUST be updated

If multiple documents are impacted:

→ ALL must be updated

---

## Documentation Update Matrix

Use the following rules to determine required updates:

### If system behavior changed:
→ update:  
docs/architecture/system_state.md

### If execution flow / control / boundaries changed:
→ update relevant files in:  
docs/architecture/

### If a new feature or capability was built:
→ update:
- build log
- design document (if applicable)

### If tool behavior or structure changed:
→ update:
- docs/design/
- tool manifests under distributions/

### If new files or directories were created:
→ update:
docs/infrastructure/neurocore_repository_map.txt

### If system-level environment changed:
→ update:
docs/infrastructure/neurocore_system_map.txt

### If screenshots were captured:
→ embed in:
build log (REQUIRED)

### If documentation structure or navigation changed:
→ update:
docs/README.md or relevant index files

---

## Build Log Standard (STRICT)

The build log is REQUIRED for every build phase.

Location:

/mnt/g/ai/projects/neurocore/build-logs/

### Build Log Rules

The build log MUST:

- reflect REAL events only
- NOT fabricate problems, errors, or decisions
- follow a consistent narrative structure
- match the style of existing build logs
- include screenshots inline (if captured)
- describe actual system evolution

### Required Structure

Each build log MUST include:

1. Starting State
2. Objective of the Phase
3. Implementation Work Performed
4. Issues Encountered (if any)
5. Debugging / Fixes Applied (if any)
6. Final Implementation State
7. Resulting System Behavior

Screenshots MUST be embedded inline at relevant points.

---

## Repository Validation Rule

Before updating ANY document:

The assistant MUST:

- verify all file paths against the repository map
- confirm file existence
- use exact paths

The assistant MUST NOT:

- invent file names
- approximate paths
- reference unknown files

If a file cannot be validated:

→ STOP and request clarification

---

## Scope Boundary Rule

The assistant MUST:

- update ONLY documentation impacted by the build phase

The assistant MUST NOT:

- rewrite unrelated documents
- perform cosmetic or stylistic rewrites outside scope
- modify documentation without a direct reason

---

## Observability Protection Rule

Documentation updates MUST NOT:

- remove or alter observability guarantees
- break traceability descriptions
- misrepresent execution flow

If documentation conflicts with observability:

→ documentation MUST be corrected

---

## Completion Gate (MANDATORY)

Before declaring documentation complete, the assistant MUST verify:

- Build log is written
- All impacted documents are updated
- All paths are validated against repository map
- Screenshots are embedded (if applicable)
- Documentation is internally consistent
- No outdated or conflicting information remains

If ANY condition fails:

→ documentation is NOT complete

---

## Output Format Requirements

The assistant MUST present documentation updates as:

1. List of files to be updated
2. Brief explanation of why each file is updated
3. FULL file replacements (no partial edits)

All files MUST be provided in:

- a single code block per file
- using four backticks (````)

---

## Resume Prompt Alignment Requirement

If the build phase introduces:

- new workflow rules
- new system behavior constraints
- new documentation requirements

The assistant MUST:

→ evaluate whether updates are required to:
docs/ai-operations/resume_prompt_compressed.md

The assistant MUST follow rules defined in:

docs/ai-operations/context_loading_strategy.md

If resume prompt updates are required:

→ they MUST be included in the closeout

---

## Context Strategy Reinforcement

If documentation behavior or workflow rules change:

The assistant MUST evaluate:

docs/ai-operations/context_loading_strategy.md

If misalignment exists:

→ the document MUST be updated

---

## Final Rule

Documentation is part of the system.

If documentation is incorrect:

→ the system is incorrect

No build phase is complete until documentation is fully aligned with reality.
