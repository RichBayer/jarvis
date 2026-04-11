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
- existing files and structure  

---

## Layer 3 – Architecture (WHEN NEEDED)

Use for design or planning:

```
docs/architecture/neurocore_master_blueprint.md
```

Optional:

```
docs/architecture/system_architecture.md
```

Provides:

- system evolution plan  
- architectural constraints  
- future direction  

---

## Layer 4 – On-Demand Context (ONLY WHEN REQUIRED)

Provide only when requested or necessary:

- specific code files  
- logs  
- error output  
- targeted documentation  

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