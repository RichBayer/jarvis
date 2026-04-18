# NeuroCore – Master Blueprint

---

# Purpose of This Document

This document defines:

- how NeuroCore evolves  
- how major capabilities are introduced  
- what systems must exist before others  
- the correct order of architectural expansion  

This is NOT:

- a vision document  
- a system architecture breakdown  
- a code-level implementation guide  

This is the control document for system evolution.

---

# System Definition

NeuroCore is a persistent, local-first AI system designed to operate as a:

> cognitive runtime platform

It is intended to:

- maintain context over time  
- reason about problems  
- take controlled actions  
- observe environmental signals  
- operate safely under defined constraints  
- recover from failure  

---

# Platform Model

NeuroCore operates as a platform.

Distributions are built on top of it.

---

## Core System

NeuroCore provides:

- runtime  
- control plane  
- execution system  
- reasoning system  
- memory systems  

---

## Distribution Layer

Distributions define how NeuroCore is used.

Example:

- Argus – system intelligence distribution  

Distributions:

- do NOT modify the runtime  
- do NOT bypass the control plane  
- operate strictly within system constraints  

---

# Current System State (Reality)

NeuroCore currently has:

- persistent daemon (UNIX socket)  
- runtime manager (central orchestration layer)  
- control plane (execution authority + policy enforcement)  
- execution engine (structured tool execution)  
- tool registry and BaseTool contract  
- CommandRunner (real system execution layer)  
- system_info tool (real, read-only execution)  
- service_manager tool (simulated execution)  
- RAG-based knowledge system  
- session memory (short-term)  
- streaming CLI interface (`ai`)  
- full trace system (end-to-end observability)  

At this stage, the system is:

> a controlled execution platform with real system interaction

---

# Transition Point

The system has moved from:

> answering questions  

to:

> performing controlled actions within an environment  

This introduces:

- execution  
- safety constraints  
- system responsibility  

---

# Core Architectural Rule

All system behavior must pass through:

> Runtime Manager → Control Plane

Nothing:

- executes  
- modifies state  
- accesses memory  
- interacts with external systems  

without passing through this path.

---

# Phase 5 – Execution & Control Architecture

Phase 5 introduces all systems required for safe, controlled execution.

This phase must be completed in order.

---

## Phase 5A – Runtime Control Plane  
Status: COMPLETE  

---

## Phase 5B – Tool Interface Standard  
Status: COMPLETE  

---

## Phase 5C – Security, Policy, Authority  
Status: IN PROGRESS  

Focus:
- execution permissions  
- policy enforcement  
- authority boundaries  

---

## Phase 5D – Observability & Tracing  
Status: COMPLETE  

Includes:
- request_id propagation  
- structured trace events  
- end-to-end visibility  

---

## Phase 5E – Evaluation & Regression  
Status: NOT IMPLEMENTED  

---

## Phase 5F – Execution Safety & Recovery  
Status: NOT IMPLEMENTED  

Will include:
- failure handling  
- retries  
- execution rollback strategy  
- timeout enforcement expansion  

---

## Phase 5G – Task / Workflow State Layer  
Status: NOT IMPLEMENTED  

---

## Phase 5H – Tool Execution Layer  
Status: COMPLETE  

Includes:
- execution engine  
- tool registry  
- BaseTool contract  
- structured execution flow  

---

## Phase 5I – Safe Local Tools  
Status: IN PROGRESS  

Includes:

- system_info (complete)  

Next required tools:

- process inspection  
- network inspection  
- disk health  
- log analysis  

---

## Phase 5J – External Threat Defense  
Status: NOT IMPLEMENTED  

---

## Phase 5K – External Tools  
Status: NOT IMPLEMENTED  

---

## Phase 5L – Security Intelligence Pipeline  
Status: NOT IMPLEMENTED  

---

## Phase 5M – Memory Expansion  
Status: NOT IMPLEMENTED  

---

## Phase 5N – Self-Reconstruction System  
Status: NOT IMPLEMENTED  

---

# Argus V1 Integration

Argus is the first distribution built on top of NeuroCore.

---

## Argus Definition

Argus is:

> a read-only system intelligence distribution  

It provides:

- system diagnostics  
- service analysis  
- log analysis  
- network inspection  
- security awareness  
- plain-English explanations  
- executive-level summaries  

---

## Argus Constraints

Argus must:

- be read-only  
- use controlled execution only  
- never bypass the control plane  
- never modify system state  

---

## Argus Dependency Mapping

Argus depends on completion of:

---

### Phase 5H – Tool Execution Layer  
Status: COMPLETE  

---

### Phase 5I – Safe Local Tools  
Status: IN PROGRESS  

Required:

- reliable system inspection tools  
- consistent output structure  
- predictable execution behavior  

---

### Phase 5C – Security / Policy (Partial)

Required:

- safe execution boundaries  
- controlled permissions  

---

## Argus Readiness Condition

Argus V1 is ready when:

- real execution is stable  
- core toolset is complete  
- outputs are consistent and readable  
- execution is safe and predictable  

---

# Development Priority (IMPORTANT)

Until Argus V1 is ready:

Focus ONLY on:

1. read-only system tools  
2. execution stability  
3. tool standardization  
4. output quality  

---

## Deferred Systems (INTENTIONAL)

These are delayed on purpose:

- perception layer  
- home automation  
- multi-user systems  
- advanced memory systems  
- external integrations  

---

# Execution Model (Reference)

All operations follow:

request  
→ runtime manager  
→ control plane  
→ execution or reasoning  
→ tool / model  
→ response  
→ tracing  

---

# System Invariants (Non-Negotiable)

## Forbidden

- bypassing the runtime  
- raw command execution outside tools  
- hidden memory writes  
- uncontrolled tool usage  
- unlogged execution  

---

## Required

- structured inputs and outputs  
- policy enforcement  
- observable execution  
- controlled memory access  
- reproducible behavior  

---

# Definition of Success

NeuroCore becomes:

- persistent  
- local-first  
- controlled  
- observable  
- secure  
- capable of action  
- capable of long-running work  
- capable of recovery  

---

# Argus V1 Success Criteria

Argus V1 is successful when:

- system issues are clearly identified  
- troubleshooting time is reduced  
- outputs are understandable to non-technical users  
- system remains safe and predictable  
- installation is simple and reliable  

---

# Final Principle

NeuroCore is the platform.  

Argus is the first product built on that platform.  

The system must evolve without breaking this separation.