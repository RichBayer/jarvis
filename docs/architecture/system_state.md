# NeuroCore System State

## Overview

NeuroCore is a local-first AI system designed to provide structured reasoning, controlled execution, and full system observability.

The system runs as a persistent daemon and processes every request through a clearly defined and enforced execution pipeline.

At this stage, NeuroCore supports:

- real system execution through system tools  
- **enforced structured data output for machine interpretation across all system tools**  
- an Argus tool layer for system-level reasoning and diagnostics  
- **multi-signal system diagnostics through aggregation tools**
- **structured CLI diagnostic output (UX layer)**
- **Phase 6 CLI output-control modes for concise, raw, summary, and JSON output**
- **raw evidence preservation across implemented Argus diagnostic tools**

---

## Current Architecture

NeuroCore follows a layered architecture:

```
CLI
→ Daemon
→ Runtime Manager
→ Control Plane
→ (Execution Engine → Argus Tool → System Tool → CommandRunner → OS)
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
- Concise default Argus diagnostic output
- Optional raw evidence display with `--raw`
- Summary-only diagnostic display with `--summary`
- Full structured response display with `--json`
- Copy/paste raw evidence hint when raw evidence exists

Notes:

- CLI is intentionally simple  
- Responsible only for input + output formatting  
- Does not contain execution logic  
- **Now provides structured diagnostic presentation (severity, findings, recommendations, controlled raw evidence visibility)**  
- Raw evidence is preserved by Argus tools but hidden by default in normal CLI output  
- Raw evidence remains available on demand through `--raw`  
- Machine-readable structured responses remain available through `--json`  

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

- Transport layer between CLI and system  
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

- Maintains separation between execution and reasoning paths  
- Ensures consistent output structure  

---

### 4. Control Plane

Location:
```
runtime/control_plane.py
```

Responsibilities:

- Request classification (execution vs reasoning)  
- Execution keyword detection (e.g. `info`, `processes`, `disk`, `memory`, `summary`, `system`)  
- Policy enforcement  
- Confirmation handling (when required)  
- Tool selection and validation  

Notes:

- Authority layer of the system  
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

- Does not execute commands directly  
- Delegates execution to tools  

---

### 6. Tool Layer

Locations:
```
tools/base_tool.py
tools/system/
tools/argus/
```

NeuroCore now has **two distinct tool layers**.

---

## System Tool Layer

Location:
```
tools/system/
```

Purpose:

- direct system interaction  
- raw signal collection  
- read-only operations  

Rules:

- uses `CommandRunner`  
- one tool = one capability  
- no aggregation  
- no interpretation  

### System Tools

- `system_info`
- `process_top`
- `disk_usage`
- `memory_usage`
- `disk_layout`
- `network_interfaces`
- `network_connections`
- `uptime_load`
- `system_logs`
- `users_sessions`
- `recent_logins`
- `service_manager` (simulated)

---

## Argus Tool Layer

Location:
```
tools/argus/
```

Purpose:

- compose system tools  
- aggregate multiple signals  
- interpret system state  
- produce diagnostic output  

Rules:

- MUST NOT call `CommandRunner`  
- MUST use system tools only  
- MUST consume structured `data`  
- MUST NOT parse formatted message output  

### Implemented Argus Tools

- `system_summary`
- `process_top_analysis`
- `memory_analysis`
- `disk_analysis`
- `network_analysis`
- `connections_analysis`
- `uptime_analysis`
- `logs_analysis`
- **system_analysis (multi-signal aggregation tool)**

---

### Tool Output Contract (CRITICAL)

All system tools now return:

```
{
  "status": "...",
  "message": "...",
  "data": { ... }
}
```

- `message` → human-readable output (CLI)  
- `data` → structured output for Argus  

This contract is now **enforced across all system tools** and is no longer optional.

Implemented Argus diagnostic tools now return:

```
{
  "status": "...",
  "message": "...",
  "data": {
    "severity": "...",
    "findings": [...],
    "recommendations": [...],
    "raw": { ... }
  }
}
```

The Phase 5J closeout aligned the remaining implemented Argus tools with this raw-evidence pattern:

- `system_summary`
- `connections_analysis`
- `uptime_analysis`
- `logs_analysis`

This completed the raw-evidence diagnostic contract across the implemented Argus tool layer.

---

### 7. Command Execution Layer

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

- Direct interface to the operating system  
- All real execution flows through this layer  

---

### 8. Reasoning Stack

Components:

- Router  
- RAG system  
- Session memory  

Responsibilities:

- Natural language interpretation  
- Query rewriting  
- Knowledge retrieval  
- LLM-based response generation  

---

## Observability System

Location:
```
runtime/tracing.py
```

Capabilities:

- Structured trace events  
- Global `request_id` per request  
- End-to-end trace continuity  

---

## Trace Flow

```
runtime_manager
→ control_plane
→ execution_engine
→ tool (argus/system)
→ command_runner (if execution)
→ return path
```

All components share the same trace context.

---

## Execution Model

### Execution Path

```
control_plane
→ execution_engine
→ argus_tool (if applicable)
→ system_tool
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

- All execution requires control plane approval  
- Tools operate in defined execution modes:
  - `auto` (safe read-only)  
  - `manual` (confirmation required)  
- Argus tools cannot execute commands directly  
- No component can bypass the control plane  

---

## Current Capabilities

NeuroCore now supports:

- Persistent daemon architecture  
- CLI + piped input support  
- Structured and streaming responses  
- Control-plane enforced execution  
- Tool-based execution framework  
- Real system command execution across multiple domains  
- **Guaranteed structured system data across all system tools**  
- **Full Argus diagnostic layer across implemented core system domains**
- **Deterministic system interpretation (severity + findings + recommendations)**
- **Raw evidence preservation across implemented Argus diagnostic tools**
- **Multi-signal system diagnostics (aggregation layer)**
- **Human-readable CLI diagnostic output (UX layer)**
- **Concise default Argus CLI output**
- **On-demand raw evidence display through `--raw`**
- **Summary-only diagnostic display through `--summary`**
- **Full structured JSON response display through `--json`**
- **Copy/paste raw evidence hints for discoverability**
- Full observability and tracing  

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

- executing real system commands across multiple domains  
- exposing structured system state  
- supporting a full diagnostic interpretation layer (Argus)  
- preserving raw evidence across implemented Argus diagnostic outputs  
- supporting multi-signal system analysis  
- presenting structured diagnostic output through the CLI  
- supporting Phase 6 CLI output-control behavior  
- fully observable end-to-end  
- stable for continued Phase 6 distribution-layer work  

---

## Next Phase

- Continue Phase 6 Distribution Layer work  
- Refine Argus ACLI output control (filtering, summarization, signal selection)  
- Improve default diagnostic readability while preserving access to raw evidence  
- Maintain strict control plane enforcement  