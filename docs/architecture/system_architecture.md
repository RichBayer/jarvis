# NeuroCore – System Architecture

---

# Purpose

This document defines the architectural structure of NeuroCore, including:

- system layers  
- execution flow  
- component responsibilities  
- system boundaries  

This document reflects actual system design and current implementation state.

---

# System Definition

NeuroCore is a:

- persistent daemon-based system  
- local-first cognitive runtime  
- control-plane governed execution system  

It is NOT:

- a stateless request/response tool  
- a simple chatbot  
- a direct command execution engine  

---

# Architectural Model

NeuroCore is composed of layered systems.

---

## Layer 1 – Distribution Layer

This layer defines how NeuroCore is exposed and packaged for users.

Examples:

- Argus (system intelligence distribution)

This layer:

- defines user experience  
- constrains system behavior  
- selects capabilities  

This layer does NOT:

- modify runtime behavior  
- bypass control plane  
- directly execute commands  

---

## Layer 2 – Interface Layer

Handles all user interaction.

Examples:

- CLI (`ai`)  
- future Argus CLI wrapper  
- future UI / voice interfaces  

Responsibilities:

- input collection  
- output streaming  
- session handling  

---

## Layer 3 – Runtime Layer (Core System)

The central execution system.

Components:

- NeuroCore Daemon  
- Runtime Manager  
- Control Plane  

Responsibilities:

- persistent system state  
- request lifecycle management  
- routing authority  
- policy enforcement  

All system activity must pass through this layer.

---

## Layer 4 – Execution Layer

Handles controlled system interaction.

Components:

- Execution Engine  
- Tool Registry  
- BaseTool contract  

Responsibilities:

- structured tool execution  
- controlled system access  
- enforcement of execution rules  

Execution Path:

```
control_plane → execution_engine → tool
```

Tools are resolved dynamically and may belong to different tool layers.

---

## Layer 5 – Tool Layer (NEW – FORMALIZED)

NeuroCore contains two tool layers.

---

### System Tool Layer

Location:

```
tools/system/
```

Purpose:

- direct system interaction  
- raw signal collection  
- read-only execution  

Responsibilities:

- execute commands via CommandRunner  
- return structured system data  
- expose system state  

---

### Argus Tool Layer

Location:

```
tools/argus/
```

Purpose:

- compose system tools  
- aggregate signals  
- interpret system state  
- produce diagnostic output  

Rules:

- MUST NOT call CommandRunner  
- MUST use system tools only  
- MUST consume structured `data`  

Current Implementation:

- `system_summary` (active)

---

## Layer 6 – Command Execution Layer

Location:

```
tools/system/command_runner.py
```

Responsibilities:

- safe subprocess execution  
- timeout enforcement  
- capture stdout / stderr / return codes  

Notes:

- only system tools interact with this layer  
- this is the only boundary to the OS  

---

## Layer 7 – Logic Layer

Responsible for reasoning and routing.

Components:

- Router (`jarvis_router.py`)

Responsibilities:

- query rewriting  
- context resolution  
- prompt construction  
- routing decisions  

Constraints:

- cannot execute commands  
- must obey control plane  

---

## Layer 8 – Knowledge Layer

Responsible for retrieval and contextual understanding.

Components:

- Chroma vector database  
- embedding model  
- retrieval system  

Capabilities:

- semantic search  
- metadata filtering  
- contextual grounding  

---

## Layer 9 – Model Layer

Responsible for AI processing.

Components:

- local LLM runtime (Ollama)

Responsibilities:

- response generation  
- reasoning support  

---

## Layer 10 – System Config Layer

Location:

```
/mnt/g/ai/system/
```

Contains:

- personalities  
- profiles  
- system state  

Responsibilities:

- define system behavior configuration  
- define user-level behavior patterns  
- support distribution customization  

---

# Execution Flow

All system interaction follows a strict pipeline:

```
Interface Layer
    ↓
UNIX Socket
    ↓
NeuroCore Daemon
    ↓
Runtime Manager
    ↓
Control Plane
    ↓

    [ Execution Path ]                         [ Reasoning Path ]

    Execution Engine                          Logic Layer (Router)
    ↓                                         ↓
    Argus Tool (if applicable)                Knowledge System
    ↓                                         ↓
    System Tool                               Model Runtime (Ollama)
    ↓
    CommandRunner
    ↓
    Operating System

    ↓
Streaming Response
```

---

# Core Architectural Rule

All behavior must pass through:

```
daemon → runtime_manager → control_plane
```

Nothing:

- executes  
- accesses memory  
- interacts with system resources  

without passing through the control plane.

---

# System Invariants

## Forbidden

- bypassing the runtime  
- raw command execution  
- uncontrolled tool usage  
- hidden memory modification  

---

## Required

- structured inputs  
- structured outputs  
- policy enforcement  
- observable execution  
- controlled system access  

---

# Argus Integration

Argus operates across two layers:

1. Distribution Layer (user-facing behavior)  
2. Tool Layer (system interpretation tools)  

Argus defines:

- system intelligence behavior  
- read-only constraints  
- diagnostic capabilities  

Argus does NOT:

- modify execution engine  
- bypass control plane  
- introduce new execution paths  

---

# Platform vs Distribution Model

NeuroCore is:

The platform (core system)

Argus is:

A distribution (product layer)

This enables:

- multiple system configurations  
- different user experiences  
- reuse of core architecture  

---

# Future Expansion Model

Additional distributions may be created:

- Argus (system intelligence)  
- HomeCore (home automation)  
- DevCore (development assistant)  

All distributions must:

- use the same runtime  
- obey the same control plane  
- use the same execution system  

---

# Design Principle

NeuroCore = Cognitive Runtime Platform  
Argus = System Intelligence Distribution  

---

# Final Rule

There is only ONE runtime.

Distributions must never create parallel systems.

All intelligence, execution, and control must remain centralized.
