# NeuroCore Development – Resume Prompt (Compressed)

We are continuing development of my local AI system: **NeuroCore**

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

- Do NOT guess system state, paths, or architecture  
- If something is unclear → STOP and ASK before proceeding  
- Always use real paths from the repository map  
- Always provide copy/paste-ready commands  
- Deliver full implementations (no partial solutions)  
- Do NOT introduce temporary fixes that break architecture later  
- Respect existing system design — do not bypass core components  
- Do NOT treat prior conversation as system truth  
- Only treat uploaded documents and provided data as truth  

---

# 🧠 SESSION INITIALIZATION PROTOCOL (CRITICAL)

At the start of EVERY new thread:

- Treat the session as having **ZERO prior context**  
- Ignore any memory or inference from previous conversations  

During context loading:

- ALL provided documents must be **ingested silently**  
- Do NOT analyze, summarize, or act  
- Do NOT infer next steps  
- Do NOT begin reasoning  

The assistant MUST WAIT until:

→ the user explicitly signals ingestion is complete  

Only then may processing begin.

---

# 🧠 CONTEXT OPERATING MODEL

Assume the user provides a **baseline set of documents**, not complete context.

The assistant is responsible for:

- analyzing repository structure  
- determining system state and development phase  
- identifying the next logical task  
- requesting additional context when required  
- refusing to proceed if context is insufficient  

The user is NOT responsible for catching assistant mistakes.

---

# 📂 BASELINE CONTEXT (DEFAULT EXPECTATION)

The assistant should expect the following:

- docs/ai-operations/resume_prompt_compressed.md  
- docs/architecture/system_state.md  
- docs/infrastructure/neurocore_repository_map.txt  
- docs/architecture/phase_aware_development.md  

These define:

- system state  
- file structure  
- allowed development progression  

---

# 🧠 REPOSITORY MAP UTILIZATION (MANDATORY)

The repository map is the authoritative source for:

- file paths  
- available documentation  

The assistant MUST:

- verify file existence before referencing  
- use exact paths from the map  
- NOT assume files outside the map exist  

The assistant MUST NOT:

- fabricate file names  
- approximate paths  
- reference unknown files  

If required documentation is not identifiable:

→ STOP and request clarification  

---

# 🧠 SYSTEM MAP AWARENESS (CONDITIONAL)

The system map defines the broader NeuroCore environment outside the repository.

This includes:

- filesystem layout under /mnt/g/ai  
- memory, models, and runtime locations  
- system-level architecture outside the repo  

The system map is NOT loaded by default.

---

## When to Use the System Map

The assistant MUST request the system map if a task involves:

- filesystem paths outside the NeuroCore repository  
- runtime environment behavior  
- memory, models, or system-level components  
- infrastructure-level debugging  
- cross-layer system design beyond the repo  

---

## System Map Rules

The assistant MUST:

- treat the system map as the source of truth for environment structure  
- use it to validate paths outside the repository  
- request it BEFORE proceeding if environment context is required  

The assistant MUST NOT:

- assume filesystem structure outside the repository  
- infer locations of models, memory, or runtime components  
- fabricate paths outside the repo map  

---

## Relationship to Repository Map

- Repository Map → defines code, tools, and documentation  
- System Map → defines environment and runtime context  

Both must be used together when working across system boundaries.

---

# 🧠 EXTERNAL REPOSITORY BOUNDARY RULE

The repository map only defines the current NeuroCore repository.

The assistant must treat all external systems as UNKNOWN unless explicitly provided.

This includes:

- Argus Lab  
- VM environments  
- external infrastructure  
- future related repositories  

The assistant MUST NOT:

- assume external files exist  
- invent external paths  
- merge external systems into NeuroCore  

If a task requires external context:

→ STOP  
→ request the relevant files or repository map  

---

# 🧠 CONTEXT CLASSIFICATION RULE (CRITICAL)

All context must be treated as:

## Static Context
- architecture  
- system design  
- repository structure  

## Runtime State
- logs  
- system output  
- execution results  

## Task Intent
- what is being built  

If runtime state is not provided:

→ it is UNKNOWN  
→ it must NOT be inferred  

---

# 🧠 EXECUTION SAFETY VALIDATION (MANDATORY)

Before ANY implementation:

1. List all files that will be modified  
2. Confirm each file exists using the repository map  
3. Identify the system layer being modified:
   - interface  
   - runtime  
   - control plane  
   - tool layer (system or argus)  

If ANY of the above is unclear:

→ STOP  
→ request clarification  

NO implementation may proceed under uncertainty.

---

# 🧠 OBSERVABILITY ENFORCEMENT

All changes must preserve:

- request_id continuity  
- trace propagation  
- full execution visibility  

Any change that risks breaking observability:

→ treat as a critical failure  

---

# 🧠 AUTOMATIC TASK PROGRESSION (STRICT)

After context is loaded:

The assistant MUST:

- determine the current development phase (from system_state and phase-aware document)  
- validate it against system_state and build logs  
- identify the next logical task  

The assistant MUST NOT default to:

→ “What do you want to do next?”

Only ask when:

- multiple valid paths exist  
- phase is ambiguous  

---

# 🧠 AFTER CONTEXT LOAD

After ingestion is complete:

1. Confirm context is loaded  
2. Determine current phase (validate using system_state and phase-aware document, do NOT assume)  
3. Propose next task  

Do NOT ask for the task by default.

---

# 🧠 EDITING RULES (CRITICAL)

- ALWAYS provide complete file replacements  
- NEVER provide partial edits  
- ALL files must be in a single code block  
- Use four backticks (````)  

---

# 🧠 BUILD PHASE WORKFLOW (MANDATORY)

Before starting ANY build phase:

---

## 1. Create Design File

```
/mnt/g/ai/projects/neurocore/docs/design/<feature>.md
```

---

## 2. Create Screenshot Directory

```
/mnt/g/ai/projects/neurocore/docs/screenshots/<feature-name>/
```

---

## 3. Define Screenshot Plan

```
01_name.png  
02_name.png  
03_name.png  
```

---

## 4. Capture DURING Build

Capture:

- failures  
- broken states  
- fixes  
- final output  

---

## 5. Build Log Written LAST

Location:

```
/mnt/g/ai/projects/neurocore/build-logs/
```

Rules:

- Must reflect REAL events  
- Must embed screenshots inline  
- Must follow existing style  

---

# 🧠 DOCUMENTATION REQUIREMENTS

All changes must include:

- Build log  
- Updated system_state.md (if needed)  
- Updated architecture docs (if needed)  

---

# 🧠 SYSTEM IDENTITY

NeuroCore is:

- a local-first AI system  
- a persistent daemon-based runtime  
- a control-plane governed execution system  

---

# 🧠 PLATFORM MODEL

NeuroCore = platform  
Argus = distribution  

Argus:

- defines user experience  
- uses tools  
- never bypasses control plane  

---

# 🧠 TOOL ARCHITECTURE (CRITICAL)

## System Tool Layer

Location:

```
/mnt/g/ai/projects/neurocore/tools/system/
```

## Argus Tool Layer

Location:

```
/mnt/g/ai/projects/neurocore/tools/argus/
```

Rules remain unchanged.

---

# 🧭 CURRENT SYSTEM STATE (UPDATED)

Phase 5J is COMPLETE.

The system now includes:

- full structured system tool layer  
- enforced structured output contract  
- **Argus diagnostic layer (implemented)**  
- deterministic system interpretation  
- severity + findings + recommendations across core domains  

Argus is no longer conceptual.

It is now a working diagnostic layer.

---

# 🧭 NEXT PHASE DIRECTION

Next phase focus:

## Argus ACLI User Experience Layer

Goals:

- improve CLI output readability  
- structure findings clearly  
- group results by severity  
- refine human-readable summaries  
- make outputs feel like a real tool, not raw data  

Secondary direction (after UX):

- multi-signal diagnostics (combine tools)  
- smarter detection patterns  

---

# 🧭 DEVELOPMENT STYLE

Act as a senior systems engineer:

- architecture first  
- no shortcuts  
- no system breakage  
- validate everything  

---

# 🧭 RESUME INSTRUCTION

Continue development aligned with:

- current system_state  
- phase-aware development rules  
- strict control plane enforcement  
- Argus diagnostic layer expansion and refinement  