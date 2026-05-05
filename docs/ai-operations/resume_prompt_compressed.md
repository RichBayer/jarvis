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
- The assistant MUST NOT modify or reinterpret system architecture  
- The assistant MUST NOT introduce new design patterns or structural changes  
- The assistant MUST strictly follow existing architecture unless explicitly instructed  

If architecture appears flawed:

→ STOP  
→ explain the issue  
→ request approval before proceeding   

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

---

# 🧠 TOOL CREATION ENFORCEMENT (CRITICAL)

When creating or modifying ANY tool:

The assistant MUST follow:

docs/design/argus_tool_creation_workflow.md

This includes:

- tool file must exist before registration  
- tool must be registered in tools/__init__.py  
- control plane must route the command  
- output contract must be complete  
- raw output must be preserved  

The assistant MUST NOT:

- reference tools before they exist  
- skip registration  
- skip validation  
- assume execution path works  

If any step is missing:

→ STOP  
→ fix the workflow  

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

(unchanged)

---

# 🧠 EXTERNAL REPOSITORY BOUNDARY RULE

(unchanged)

---

# 🧠 CONTEXT CLASSIFICATION RULE (CRITICAL)

(unchanged)

---

# 🧠 EXECUTION SAFETY VALIDATION (MANDATORY)

(unchanged)

---

# 🧠 OBSERVABILITY ENFORCEMENT

(unchanged)

---

# 🧠 AUTOMATIC TASK PROGRESSION (STRICT)

(unchanged)

---

# 🧠 AFTER CONTEXT LOAD

(unchanged)

---

# 🧠 EDITING RULES (CRITICAL)

(unchanged)

---

# 🧠 BUILD PHASE WORKFLOW (MANDATORY)

(unchanged)

---

# 🧠 DOCUMENTATION REQUIREMENTS

(unchanged)

---

# 🧠 DOCUMENTATION CLOSEOUT RULES (CRITICAL)

During documentation closeout:

- Do NOT make unknown documentation changes  
- Do NOT silently rewrite existing prose  
- Do NOT perform style cleanup unless explicitly requested  
- Do NOT restructure sections unless required by the current change  
- Explain the exact intended documentation changes before providing a full-file replacement  
- Only update content directly impacted by the build phase or explicit user request  
- Preserve unchanged sections unless modification is necessary to add verified new details  

If a broader cleanup or rewrite would improve a document:

→ STOP  
→ explain the optional improvement  
→ request explicit approval before including it  

---

# 🧠 SYSTEM IDENTITY

(unchanged)

---

# 🧠 PLATFORM MODEL

(unchanged)

---

# 🧠 TOOL ARCHITECTURE (CRITICAL)

(unchanged)

---

# 🧭 CURRENT SYSTEM STATE (UPDATED)

Phase 5J is COMPLETE.

Important closeout correction:

Phase 5J should be considered complete only after the raw-evidence contract closeout documented in:

build-logs/025_system_analysis_multi_signal.md

The closeout aligned the remaining implemented Argus tools with the raw-evidence diagnostic contract:

- `tools/argus/connections_analysis.py`
- `tools/argus/uptime_analysis.py`
- `tools/argus/logs_analysis.py`
- `tools/argus/system_summary.py`

These tools now match the raw-evidence pattern already established by:

- `tools/argus/disk_analysis.py`
- `tools/argus/memory_analysis.py`
- `tools/argus/network_analysis.py`
- `tools/argus/process_top.py`
- `tools/argus/system_analysis.py`

Phase 6A output-control pass is COMPLETE.

The first Phase 6 output-control pass is documented in:

build-logs/026_phase_6_argus_acli_output_control.md  
docs/design/phase_6_argus_acli_output_control.md

Phase 6 output-control continuation is COMPLETE.

The continuation pass is documented in:

build-logs/027_phase_6_argus_acli_completion.md  
docs/design/phase_6_argus_acli_output_control.md  
docs/design/argus_acli_user_experience_layer.md  
docs/distributions/argus/acli_spec.md  

The system now includes:

- full structured system tool layer  
- enforced structured output contract  
- Argus diagnostic layer across implemented core domains  
- deterministic system interpretation  
- severity + findings + recommendations across implemented Argus tools  
- **raw evidence preserved through implemented Argus diagnostic outputs**
- **multi-signal system aggregation (`system_analysis`)**
- **structured CLI diagnostic UX layer**
- **human-readable diagnostics backed by real system data**
- **Phase 6 CLI output-control behavior**
- **concise default Argus diagnostic output**
- **on-demand raw evidence display through `--raw`**
- **summary-only diagnostic display through `--summary`**
- **full structured JSON response display through `--json`**
- **copy/paste raw evidence hints for discoverability**
- **report-style diagnostic formatting**
- **severity-sorted findings**
- **component/severity finding labels**
- **display-only severity filtering through `--severity`**
- **display-only signal filtering through `--signal`**
- **combined signal + severity filtering**
- **filtered recommendation labeling**
- **command-name-aware CLI behavior (`ai` vs `acli`)**
- **Argus-facing `acli` command available via symlink**

Validated Phase 5J closeout behavior:

- `ai "summary"` returns interpreted output with raw evidence  
- `ai "connections"` returns interpreted output with raw evidence  
- `ai "uptime"` returns interpreted output with raw evidence  
- `ai "logs"` returns interpreted output with a raw evidence field  

Validated Phase 6A output-control behavior:

- `ai "disk"` returns concise diagnostic output with a raw evidence hint  
- `ai --raw "disk"` returns diagnostic output with raw evidence displayed  
- `ai --summary "disk"` returns title, severity, and raw evidence hint only  
- `ai --json "disk"` returns the full structured JSON response  
- `ai "memory"` confirms output-control behavior works beyond disk analysis  
- `ai "system"` confirms output-control behavior works with multi-signal analysis  

Validated Phase 6 output-control continuation behavior:

- `ai --severity WARN "system"` filters displayed findings by severity  
- `ai --signal disk "system"` filters displayed findings by component/signal  
- `ai --signal disk --severity WARN "system"` combines display filters  
- `ai --json --signal disk "system"` confirms JSON remains unfiltered  
- `ai --raw --signal disk "system"` confirms raw evidence remains available  
- `ai --summary --signal disk "system"` confirms summary mode remains summary-only  
- `acli system` works as the Argus-facing command form  
- `acli system --signal disk` supports target-first filtering  
- `acli system --severity WARN` supports target-first severity filtering  
- `acli --raw system` displays raw evidence through the `acli` command  
- `acli --json system` preserves full structured JSON output  
- `acli disk`, `acli memory`, `acli network`, and `acli logs` work as direct diagnostic commands  

Known note:

- `logs_analysis` may show an empty raw log section when the underlying system log command returns no visible log output. This is acceptable because the raw field is preserved and exposed.

Argus is no longer conceptual.

It is now a working diagnostic system capable of:

- multi-domain visibility  
- aggregated system state  
- individual domain diagnostics  
- human-readable diagnostics backed by real system data  
- deterministic first-pass interpretation before future model reasoning  
- controlled CLI presentation for concise, raw, summary, JSON, filtered, and signal-focused output modes  
- Argus-facing ACLI usage through the `acli` command  

---

# 🧭 NEXT PHASE DIRECTION (UPDATED)

Current completed phase work:

## Phase 6 – Distribution Layer / Argus ACLI Output Control

Completed:

- concise default Argus diagnostic output  
- `--raw` mode for raw evidence inspection  
- `--summary` mode for quick health checks  
- `--json` mode for full machine-readable response output  
- copy/paste raw evidence hints  
- report-style diagnostic formatting  
- severity-sorted findings  
- component/severity finding labels  
- display-only severity filtering  
- display-only signal filtering  
- combined signal + severity filtering  
- filtered recommendation labeling  
- command-name-aware behavior (`ai` vs `acli`)  
- Argus-facing `acli` command availability  
- validation across disk, memory, network, logs, and multi-signal system analysis  

Important UX direction:

Argus ACLI should be easy and natural for homelab users while remaining powerful for advanced users.

The intended UX supports:

- natural / fuzzy interaction:
  - `acli "what's wrong with my system?"`
  - `acli "why is disk warning?"`
  - `acli "what should I check next?"`

- direct command usage:
  - `acli system`
  - `acli disk`
  - `acli memory`
  - `acli network`
  - `acli logs`

- power-user control:
  - `acli system --signal disk`
  - `acli system --severity WARN`
  - `acli system --signal disk --severity WARN`
  - `acli --raw system`
  - `acli --json system`

Natural-language routing remains part of the Argus direction, but it must NOT be implemented inside the CLI formatter.

Future natural-language routing belongs in:

router → reasoning → control plane

Recommended next work:

## Phase 6B / Next Distribution-Layer Work

Potential next tasks:

- decide whether to create a dedicated `distributions/argus/cli/acli.py` implementation or continue sharing `scripts/ai_cli.py` temporarily  
- continue improving multi-signal presentation if needed  
- begin planning the actual ACLI distribution structure  
- clarify install/symlink behavior for `acli`  
- prepare for natural-language routing through the correct router/control-plane path  
- keep presentation behavior in the interface/distribution layer  
- keep diagnostic logic inside Argus tools  

This phase prepares the system for:

- real-world usability  
- repeated diagnostic workflows  
- future model integration  
- Argus ACLI distribution behavior  

---

## Secondary Direction (After Output Control)

- initial runtime packaging  
- filesystem layout planning  
- deeper multi-signal correlation  
- improved detection logic  
- reduction of false positives  
- better log interpretation  
- incident memory design/implementation if explicitly selected and phase-aligned  

Deferred beyond the current output-control lane:

- broad natural-language command routing inside CLI  
- model/router fuzzy intent reasoning inside CLI  

Natural-language routing itself remains planned, but it must be implemented through the correct router / reasoning / control-plane path, not as hidden CLI guessing.

---

# 🧭 DEVELOPMENT STYLE

(unchanged)

---

# 🧭 RESUME INSTRUCTION

Continue development aligned with:

- current system_state  
- phase-aware development rules  
- strict control plane enforcement  
- completed Phase 5J raw-evidence contract closeout  
- completed Phase 6A output-control pass  
- completed Phase 6 output-control continuation  
- Phase 6 Distribution Layer work  
- Argus ACLI output control and signal management  
- Argus-facing `acli` command direction  
- natural + direct + power-user ACLI UX model  
- documentation closeout surgical-update rules  