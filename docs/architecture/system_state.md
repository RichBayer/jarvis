# NeuroCore System State

## Overview

NeuroCore is a local-first AI system designed to provide structured reasoning, controlled execution, and full system observability.

The system operates as a persistent daemon and processes requests through a clearly defined execution pipeline.

---

## Current Architecture

NeuroCore follows a layered architecture:

```
CLI
→ Daemon
→ Runtime Manager
→ Control Plane
→ (Execution Engine → Tool) OR (Router → Knowledge → Model)
```

---

## Core Components

### 1. CLI Interface

Location:
```
scripts/ai_cli.py
```

Capabilities:

- Direct query execution (`ai "query"`)
- Streaming responses
- Piped input support (`command | ai`)
- Automatic trace context generation

---

### 2. Daemon

Location:
```
runtime/neurocore_daemon.py
```

Responsibilities:

- Persistent socket listener (`/tmp/neurocore.sock`)
- Request normalization
- Trace context preservation
- Routing requests to runtime manager

---

### 3. Runtime Manager

Location:
```
runtime/runtime_manager.py
```

Responsibilities:

- Entry point for all requests
- Ambiguity detection
- Execution vs reasoning path selection
- Streaming response orchestration

---

### 4. Control Plane

Location:
```
runtime/control_plane.py
```

Responsibilities:

- Request classification (execution vs reasoning)
- Policy enforcement
- Confirmation handling
- Tool selection and validation

---

### 5. Execution Engine

Location:
```
tools/execution_engine.py
```

Responsibilities:

- Tool lookup
- Input validation
- Execution orchestration
- Full trace propagation to tools

---

### 6. Tool Layer

Location:
```
tools/system/service_manager.py
```

Current State:

- Simulated execution
- Fully instrumented with tracing
- Receives full request context (not just input)

---

### 7. Reasoning Stack

Components:

- Router (`jarvis_router.py`)
- RAG system (`query_knowledge.py`)
- Session memory (`session_memory.py`)

---

## Observability System

Location:
```
runtime/tracing.py
```

Capabilities:

- Structured trace events
- Global `request_id` per request
- End-to-end trace continuity across all layers

---

## Trace Flow

Each request generates a unique `request_id` and flows through:

```
runtime_manager
→ control_plane
→ execution_engine (if execution)
→ tool (if execution)
→ back through system
```

All components share the same trace context.

---

## Execution Model

### Execution Path

```
control_plane
→ execution_engine
→ tool
```

### Reasoning Path

```
control_plane
→ router
→ knowledge
→ model
```

---

## Safety Model

- Execution requires explicit confirmation
- Tools operate in controlled modes (manual, dry-run, auto)
- No execution occurs without control plane approval

---

## Current Capabilities

- Persistent daemon architecture
- Streaming responses
- CLI + piped input support
- RAG-based reasoning
- Session memory with query rewriting
- Control-plane enforced execution
- Tool-based execution framework
- Confirmation-based safety model
- Full system observability (NEW)

---

## Key Invariant

All requests must follow:

```
daemon → runtime_manager → control_plane → system
```

No component bypasses the control plane.

---

## System Status

NeuroCore is now:

- Fully observable
- Deterministic in execution flow
- Traceable end-to-end
- Architecturally stable for expansion

---

## Next Phase

- Replace simulated tools with real system tools
- Maintain observability guarantees
- Expand execution capabilities safely