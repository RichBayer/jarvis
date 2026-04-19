# NeuroCore – Platform Ecosystem

---

# Purpose

This document defines the complete system ecosystem for:

- NeuroCore (platform)  
- Argus (distribution)  
- Homelab (training and validation environment)  

It establishes:

- system relationships  
- separation of responsibilities  
- development progression model  
- productization boundaries  

This document is the authoritative reference for how all systems interact.

---

# Core System Model

The ecosystem follows a strict layered model:

NeuroCore = Platform  
Argus = Distribution  
Homelab = Training + Validation System  

Each layer has a defined role and must not violate system boundaries.

---

# System Roles

## NeuroCore (Platform)

NeuroCore is the core runtime system.

It provides:

- persistent daemon architecture  
- runtime manager (orchestration layer)  
- control plane (execution authority)  
- execution engine (tool orchestration)  
- system tool layer (real system interaction)  
- Argus tool layer (composition and interpretation)  
- reasoning stack (router, RAG, model)  
- observability (trace system)  

NeuroCore is responsible for:

- all execution  
- all reasoning  
- all memory access  
- all system interaction  

All behavior is governed by the control plane.

---

## Argus (Distribution)

Argus is the first distribution built on NeuroCore.

It defines:

- user-facing behavior  
- diagnostic capabilities  
- system intelligence output  

Argus operates entirely within NeuroCore.

Argus does NOT:

- modify the runtime  
- bypass the control plane  
- execute commands directly  

---

## Argus Architecture

Argus operates across two layers:

### 1. Distribution Layer

Defines:

- CLI behavior (ACLI)  
- interaction model  
- output format  
- user experience  

---

### 2. Tool Layer (Argus Tools)

Location:

```
/mnt/g/ai/projects/neurocore/tools/argus/
```

Purpose:

- compose system tools  
- aggregate system signals  
- interpret system state  
- produce diagnostic output  

Rules:

- MUST NOT call CommandRunner  
- MUST use system tools only  
- MUST consume structured system data (`data`)  
- MUST NOT parse formatted message output  

---

## Homelab (Training & Validation System)

The homelab is an external system used for validation.

It provides:

- realistic infrastructure environments  
- controlled failure scenarios  
- multi-node system behavior  
- testing targets for Argus tools  

Homelab is NOT part of NeuroCore runtime.

It is:

- a validation environment  
- a training system  
- a controlled testing platform  

---

# System Interaction Model

---

## NeuroCore ↔ Argus

- Argus tools execute through NeuroCore  
- NeuroCore enforces all execution rules  
- Argus consumes structured system data  
- Argus produces interpreted output  

---

## NeuroCore ↔ Homelab

- NeuroCore connects to homelab systems  
- executes read-only inspection commands  
- collects system data  
- analyzes system behavior  

---

## Argus ↔ Homelab

- Argus interprets homelab system state  
- provides diagnostics and guidance  
- identifies system issues  

---

# Development Progression Model

The ecosystem evolves in a strict sequence.

---

## Phase 1–4 (Complete)

- runtime foundation  
- reasoning system  
- knowledge system  
- CLI interface  

---

## Phase 5 – Execution & Control Architecture (Current)

Includes:

- control plane  
- execution engine  
- tool registry  
- system tool layer  
- structured data model  
- Argus tool layer (active)  

---

## Phase 5J – Argus Tool Layer (In Progress)

Focus:

- composition tools  
- signal aggregation  
- system interpretation  

Current state:

- system_summary implemented  
- structured data model in place  
- repeatable tool pattern established  

---

## Future Phases

- evaluation systems  
- feedback loops  
- structured training platforms  
- scenario automation  
- intelligence pipelines  

---

# Current Development Position

NeuroCore is currently in:

Phase 5 – Execution & Control Architecture  

Specifically:

- Phase 5H – Tool Execution Layer → COMPLETE  
- Phase 5I – Safe Local Tools → COMPLETE  
- Phase 5J – Argus Tool Layer → IN PROGRESS  

---

# What This Means

At this stage:

- NeuroCore performs controlled execution across multiple system domains  
- a complete read-only system tool layer exists  
- system tools return structured data for machine interpretation  
- the Argus tool layer is active (system_summary implemented)  
- a repeatable Argus tool pattern is established  
- the homelab can be used for validation  

The system is NOT yet ready for:

- evaluation systems  
- feedback loops  
- structured training systems  
- scenario automation  
- intelligence pipelines  

---

# Current Development Priority

Development must focus on:

- expanding the Argus tool layer  
- consuming structured system data  
- reusing established tool patterns  
- producing structured diagnostics  
- maintaining control plane enforcement  
- preserving observability  
- preventing architectural drift  

---

# Argus Constraints (Current Phase)

Argus is limited to:

- system inspection  
- diagnostics  
- log analysis  
- structured signal aggregation  
- system state interpretation  

Argus must operate as:

- a read-only interpretation layer  
- a composition layer on top of system tools  

Argus must NOT:

- call CommandRunner  
- execute commands directly  
- modify system state  
- bypass the control plane  

Argus must NOT yet include:

- evaluation logic  
- scoring systems  
- training workflows  
- automated scenario generation  

---

# Productization Boundary

NeuroCore:

- internal platform  
- full system control  
- development environment  

Argus:

- distributable product  
- system intelligence layer  

Homelab:

- training and validation system  
- not distributed  

---

# Final Principle

NeuroCore is the platform.  
Argus is the product layer.  
Homelab is the validation environment.  

Each layer must evolve independently without breaking system boundaries.
