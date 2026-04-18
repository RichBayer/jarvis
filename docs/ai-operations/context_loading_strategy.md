# NeuroCore – Context Loading Strategy

---

# Purpose

This document defines how to efficiently provide context to ChatGPT when working on NeuroCore.

The goal is to:

- maintain accurate system awareness  
- avoid unnecessary context overload  
- ensure high-quality, system-specific responses  
- enable fast and consistent development  

---

# Core Principle

Provide **only the minimum context required** for the task.

Too little context → incorrect assumptions  
Too much context → slower, less precise responses  

---

# Context Layers

All sessions should use a layered approach:

---

## Layer 1 – Behavior (ALWAYS REQUIRED)

```
docs/ai-operations/resume_prompt_compressed.md
```

Provides:

- rules of operation  
- build philosophy  
- execution style  
- system identity  
- architectural guardrails  

---

## Layer 2 – System Awareness (DEFAULT)

Use for most work (build, changes, analysis):

```
docs/architecture/system_state.md
docs/infrastructure/neurocore_repository_map.txt
```

Provides:

- current capabilities  
- system behavior  
- execution model  
- observability guarantees  
- file structure and locations  

---

## Layer 3 – Architecture (WHEN NEEDED)

Use for design, planning, or deep system changes:

```
docs/architecture/neurocore_master_blueprint.md
```

Optional:

```
docs/architecture/system_architecture.md
docs/architecture/control_plane.md
docs/architecture/tool_execution.md
```

Provides:

- system evolution plan  
- architectural constraints  
- execution model details  
- control plane and tool behavior  

---

## Layer 4 – On-Demand Context (ONLY WHEN REQUIRED)

Provide only when necessary:

- specific code files  
- logs  
- error output  
- targeted documentation  

---

# Observability Awareness (CRITICAL)

NeuroCore is now fully traceable.

All work must preserve:

- request_id continuity  
- trace context propagation across all layers  
- visibility into execution and decision-making  

If a change risks breaking trace continuity:

→ it must be treated as a critical issue  

---

# Standard Session Types

---

## Build / Implementation (Most Common)

Upload:

- resume_prompt_compressed.md  
- system_state.md  
- neurocore_repository_map.txt  

Then provide:

```
Task: <what needs to be built>
```

---

## Architecture / Design

Upload:

- resume_prompt_compressed.md  
- neurocore_master_blueprint.md  

Optional:

- system_architecture.md  
- control_plane.md  
- tool_execution.md  

---

## Debugging

Upload:

- resume_prompt_compressed.md  
- system_state.md  

Then provide:

- error output  
- logs  
- relevant files  

---

# Assistant Behavior Expectations

The assistant must:

- NOT assume files exist without confirmation  
- use repository map for file awareness  
- ask for missing files before proceeding  
- provide exact file paths when referencing files  
- align all work with current system state  
- preserve trace context in all implementations  
- never introduce changes that break observability  

---

# What NOT to Upload by Default

Avoid sending:

- full repository dumps  
- screenshots  
- build logs  
- vision documents  
- unrelated documentation  

These should only be provided when specifically needed.

---

# Guiding Rule

If a file is not provided:

→ it should be treated as unknown  

→ not guessed  

---

# Long-Term Goal

NeuroCore should eventually:

- load its own system state  
- reason over its own architecture  
- operate without external prompting  

This strategy is a temporary bridge toward that capability.