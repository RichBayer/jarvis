# NeuroCore System State

## Overview

NeuroCore is a local-first AI system designed to provide structured reasoning, controlled execution, and full system observability.

The system runs as a persistent daemon and processes every request through a clearly defined and enforced execution pipeline.

At this point, NeuroCore is no longer just routing logic—it now executes real system commands through a controlled tool layer.

---

## Current Architecture

NeuroCore follows a layered architecture:

```
CLI
→ Daemon
→ Runtime Manager
→ Control Plane
→ (Execution Engine → Tool → OS)
   OR
→ (Router → Knowledge → Model)
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
- JSON response parsing and clean output formatting
- Piped input support (`command | ai`)
- Automatic trace context generation

Notes:

- CLI is intentionally simple
- Responsible only for input + output formatting
- Does not contain execution logic

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
- JSON serialization of responses (critical boundary)

Notes:

- The daemon is the transport layer between CLI and system
- Improper serialization here breaks the entire pipeline

---

### 3. Runtime Manager

Location:
```
runtime/runtime_manager.py
```

Responsibilities:

- Entry point for all requests
- Execution vs reasoning path selection
- Request normalization for downstream components
- Response formatting for CLI compatibility

Notes:

- Maintains clean separation between execution and reasoning paths
- Ensures consistent output structure

---

### 4. Control Plane

Location:
```
runtime/control_plane.py
```

Responsibilities:

- Request classification (execution vs reasoning)
- Execution keyword detection (e.g. `info`)
- Policy enforcement
- Confirmation handling (when required)
- Tool selection and validation

Notes:

- This is the authority layer of the system
- No execution occurs without passing through the control plane

---

### 5. Execution Engine

Location:
```
tools/execution_engine.py
```

Responsibilities:

- Tool lookup via registry
- Input validation
- Execution orchestration
- Full trace propagation to tools

Notes:

- Execution engine does not execute commands directly
- Delegates execution to tools

---

### 6. Tool Layer

Locations:
```
tools/base_tool.py
tools/system/
```

Current Tools:

- `service_manager` (simulated)
- `system_info` (real execution)

Capabilities:

- Structured input validation
- Execution mode handling:
  - `auto` (no confirmation, read-only)
  - `manual` (requires confirmation)
  - `dry-run` (future)
- Full trace context access

---

### 7. Command Execution Layer (NEW)

Location:
```
tools/system/command_runner.py
```

Responsibilities:

- Safe subprocess execution
- Timeout enforcement (10s default)
- Capture of:
  - stdout
  - stderr
  - return codes

Notes:

- This is the first direct interface to the operating system
- All real system interaction flows through this layer

---

### 8. Reasoning Stack

Components:

- Router (`jarvis_router.py`)
- RAG system (`query_knowledge.py`)
- Session memory (`session_memory.py`)

Responsibilities:

- Natural language interpretation
- Query rewriting
- Knowledge retrieval
- Response generation (LLM path)

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
→ tool
→ command_runner (if real execution)
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
→ command_runner
→ OS
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

- Execution requires control plane approval
- Tools operate in defined execution modes:
  - `auto` (safe read-only operations)
  - `manual` (requires confirmation)
- Real system execution is constrained through tool definitions
- No component can bypass the control plane

---

## Current Capabilities

NeuroCore now supports:

- Persistent daemon architecture
- Streaming and structured responses
- CLI + piped input support (`| ai`)
- RAG-based reasoning
- Session memory with query rewriting
- Control-plane enforced execution
- Tool-based execution framework
- Real system command execution (NEW)
- JSON-based daemon response model
- CLI-side JSON parsing and formatting
- Full system observability and tracing

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

- Executing real system commands
- Fully observable end-to-end
- Deterministic in execution flow
- Structurally stable for expansion

This is the first point where the system moves beyond architecture and into real capability.

---

## Next Phase

- Expand system toolset (process, network, disk health, logs)
- Improve output formatting for usability
- Introduce intelligent tool selection (natural language → tool mapping)
- Maintain strict control plane enforcement as capabilities grow