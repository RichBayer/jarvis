# NeuroCore System State

## Overview

NeuroCore is a local-first AI system designed to provide structured reasoning, controlled execution, and full system observability.

The system runs as a persistent daemon and processes every request through a clearly defined and enforced execution pipeline.

At this stage, NeuroCore supports:

- real system execution through system tools  
- enforced structured data output for machine interpretation across all system tools  
- an Argus tool layer for system-level reasoning and diagnostics  
- multi-signal system diagnostics through aggregation tools
- structured CLI diagnostic output (UX layer)
- Phase 6 CLI output-control modes for concise, raw, summary, and JSON output
- raw evidence preservation across implemented Argus diagnostic tools
- display-only filtering controls (severity + signal)
- command-name-aware CLI behavior (ai vs acli)

---

## Current Architecture

NeuroCore follows a layered architecture:

CLI  
→ Daemon  
→ Runtime Manager  
→ Control Plane  
→ (Execution Engine → Argus Tool → System Tool → CommandRunner → OS)  
OR  
→ (Router → Knowledge → Model)

---

## Core Components

### 1. CLI Interface

Location:

scripts/ai_cli.py

Capabilities:

- Direct query execution (`ai "query"` / `acli "query"`)
- JSON response parsing and clean output formatting
- Piped input support (`command | ai`)
- Automatic trace context generation
- Concise default Argus diagnostic output
- Optional raw evidence display with `--raw`
- Summary-only diagnostic display with `--summary`
- Full structured response display with `--json`
- Display-only severity filtering (`--severity`)
- Display-only signal filtering (`--signal`)
- Combined filtering (`--signal` + `--severity`)
- Command-name-aware raw evidence hints (ai vs acli)
- Copy/paste raw evidence hint when raw evidence exists

Notes:

- CLI is intentionally simple  
- Responsible only for input + output formatting  
- Does not contain execution logic  
- Provides structured diagnostic presentation (severity, findings, recommendations, controlled raw evidence visibility)  
- Raw evidence is preserved by Argus tools but hidden by default  
- Raw evidence remains available on demand through `--raw`  
- Machine-readable structured responses remain available through `--json`  

---

### 2. Daemon

Location:

runtime/neurocore_daemon.py

Responsibilities:

- Persistent socket listener (`/tmp/neurocore.sock`)
- Request normalization
- Trace context preservation
- Routing requests to runtime manager
- JSON serialization of responses (critical boundary)

---

### 3. Runtime Manager

Location:

runtime/runtime_manager.py

Responsibilities:

- Entry point for all requests  
- Execution vs reasoning path selection  
- Request normalization for downstream components  
- Response formatting for CLI compatibility  

---

### 4. Control Plane

Location:

runtime/control_plane.py

Responsibilities:

- Request classification (execution vs reasoning)  
- Execution keyword detection  
- Policy enforcement  
- Confirmation handling  
- Tool selection and validation  

---

### 5. Execution Engine

Location:

tools/execution_engine.py

Responsibilities:

- Tool lookup via registry  
- Input validation  
- Execution orchestration  
- Full trace propagation to tools  

---

### 6. Tool Layer

Locations:

tools/base_tool.py  
tools/system/  
tools/argus/

NeuroCore has two tool layers:

---

## System Tool Layer

Purpose:

- direct system interaction  
- raw signal collection  
- read-only operations  

---

## Argus Tool Layer

Purpose:

- aggregate signals  
- interpret system state  
- produce structured diagnostics  

---

### Tool Output Contract

System tools return:

{
  "status": "...",
  "message": "...",
  "data": { ... }
}

Argus tools return:

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

---

## Current Capabilities

NeuroCore now supports:

- Persistent daemon architecture  
- CLI + piped input support  
- Structured and streaming responses  
- Control-plane enforced execution  
- Tool-based execution framework  
- Real system command execution across multiple domains  
- Guaranteed structured system data  
- Full Argus diagnostic layer  
- Deterministic system interpretation (severity + findings + recommendations)  
- Raw evidence preservation  
- Multi-signal diagnostics  
- Human-readable CLI output  
- Concise default output  
- Raw evidence on demand (`--raw`)  
- Summary mode (`--summary`)  
- JSON output (`--json`)  
- Severity filtering (`--severity`)  
- Signal filtering (`--signal`)  
- Combined filtering  
- Command-name-aware CLI behavior (`ai` vs `acli`)  
- Full observability and tracing  

---

## System Status

NeuroCore is now:

- executing real system commands  
- exposing structured system state  
- supporting full diagnostic interpretation  
- preserving raw evidence  
- supporting multi-signal analysis  
- presenting structured CLI diagnostics  
- supporting Phase 6 output-control behavior  
- supporting display-only filtering controls  
- supporting command-name-aware CLI usage (`ai` and `acli`)  
- stable for continued distribution-layer work  

---

## Next Phase

- Continue Phase 6 Distribution Layer work  
- Expand natural-language routing (outside CLI layer)  
- Improve multi-signal presentation  
- Maintain strict control plane enforcement  