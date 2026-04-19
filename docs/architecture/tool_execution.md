````markdown
# NeuroCore – Tool Execution Architecture

---

# Purpose

The Tool Execution layer is responsible for performing controlled system actions inside NeuroCore.

It ensures that:

- all execution flows through a single controlled path  
- no component executes system actions directly outside approved layers  
- execution is validated, authorized, and observable  
- system safety is enforced at all times  

At this stage, this layer is fully implemented and actively executing real system commands through controlled system tools.

It has also been extended to support the Argus composition layer without breaking execution boundaries.

---

# Core Principle

All execution must pass through the execution engine.

No tool is called directly by:

- the router  
- the model  
- the CLI / ACLI  
- any external input  
- any component outside the approved execution path  

Execution flow is strictly enforced.

---

# System Invariant

All requests must follow:

```text
daemon → runtime_manager → control_plane → system
```

No component bypasses the control plane.

---

# Execution Flow

## Top-Level Execution Flow

All execution requests follow this path:

```text
client
→ daemon
→ runtime_manager
→ control_plane
→ execution_engine
→ tool
→ runtime_manager
→ daemon
→ client
```

---

## Real System Execution Path

```text
client
→ daemon
→ runtime_manager
→ control_plane
→ execution_engine
→ system_tool
→ command_runner
→ operating system
→ system_tool
→ execution_engine
→ control_plane
→ runtime_manager
→ daemon
→ client
```

---

## Argus Composition Execution Path (ACTIVE)

```text
client
→ daemon
→ runtime_manager
→ control_plane
→ execution_engine
→ argus_tool
→ system_tool(s)
→ command_runner (inside system tools)
→ argus_tool
→ execution_engine
→ runtime_manager
→ daemon
→ client
```

---

# Architectural Role

The Tool Execution layer consists of:

- Execution Engine (orchestration)  
- Tool Registry (tool discovery)  
- BaseTool contract (standard interface)  
- System Tool Layer (execution primitives)  
- Argus Tool Layer (composition and interpretation)  
- CommandRunner (OS execution boundary)  

Each layer has distinct responsibilities and must remain separated.

---

# Execution Engine

Location:

```text
tools/execution_engine.py
```

Responsibilities:

- receive authorized execution requests from the control plane  
- resolve tools from the registry  
- validate input  
- invoke tool execution  
- return structured results  
- propagate trace context  

Notes:

- the execution engine dispatches the top-level tool  
- it does NOT recursively dispatch internal tool calls  
- Argus tools call system tools directly without re-entering the engine  

---

# Tool Registry

Location:

```text
tools/tool_registry.py
```

Responsibilities:

- maintain tool availability  
- resolve tools by name  
- enforce a single controlled registry  

---

# BaseTool Contract

Location:

```text
tools/base_tool.py
```

Defines:

- tool identity  
- input schema  
- validation logic  
- execution behavior  
- result structure  

All tools must inherit from BaseTool.

---

# Tool Interface

## Current Model

```text
tool.execute(request)
```

Tools receive:

- full request object  
- validated input  
- trace context  

---

# Request Structure

```json
{
  "tool": "...",
  "input": { ... },
  "trace": {
    "request_id": "...",
    "source": "...",
    "metadata": {}
  }
}
```

---

# Tool Layer Separation

NeuroCore has two distinct tool layers.

---

## 1. System Tool Layer

Location:

```text
tools/system/
```

Purpose:

- perform focused system execution  
- gather raw system signals  
- expose structured system state  

Rules:

- uses CommandRunner  
- one tool = one capability  
- no aggregation  
- no interpretation  

System tools MUST:

- return structured output:

```json
{
  "status": "...",
  "message": "...",
  "data": { ... }
}
```

---

## 2. Argus Tool Layer

Location:

```text
tools/argus/
```

Purpose:

- compose multiple system tools  
- aggregate signals  
- interpret system state  
- produce diagnostic output  

Rules:

- MUST NOT call CommandRunner  
- MUST use system tools  
- MUST consume structured `data`  
- MUST NOT parse formatted message output  

---

# Command Execution Layer

Location:

```text
tools/system/command_runner.py
```

Responsibilities:

- execute subprocess commands  
- enforce timeouts  
- capture stdout, stderr, return codes  

Notes:

- only system tools interact with CommandRunner  
- Argus tools never interact with it  

---

# Current Execution Model

The active execution model is:

```text
control_plane → execution_engine → argus_tool (if applicable) → system_tool → command_runner
```

---

# Why the Separation Matters

Strict separation ensures:

- execution remains controlled and auditable  
- system access remains predictable  
- Argus cannot bypass platform safety  
- reasoning and execution responsibilities remain distinct  

---

# Tool Responsibilities

## System Tools

- perform execution  
- return structured system data  
- remain narrow in scope  
- do not interpret  

---

## Argus Tools

- consume system tool data  
- aggregate signals  
- interpret findings  
- produce recommendations  

---

# Output Model

## System Tools

Return:

- raw system signals  
- structured data  

---

## Argus Tools

Return:

- interpreted findings  
- severity classification  
- recommended actions  

---

# Execution Modes

- `auto` → immediate execution  
- `manual` → requires confirmation  
- `dry-run` → advisory only  

---

# Safety Model

The system enforces:

- no execution without control plane approval  
- no direct execution from router or model  
- no CLI bypass  
- strict tool validation  
- CommandRunner isolation  
- Argus read-only enforcement  

---

# Observability Integration

Execution is fully traceable across:

- execution engine  
- argus tools  
- system tools  
- command runner  

All operations share a single request trace.

---

# Current Status

Execution Engine: COMPLETE  
Tool Registry: COMPLETE  
BaseTool Contract: COMPLETE  
System Tool Layer: ACTIVE  
CommandRunner: ACTIVE  
Real System Execution: ACTIVE  
Argus Tool Layer: ACTIVE (system_summary implemented)  

---

# Outcome

The execution architecture now supports:

- controlled system execution  
- structured system data  
- an interpretation layer (Argus)  
- strict safety boundaries  
- full observability  

---

# Next Step

- expand Argus tool layer  
- implement process_top (Argus version)  
- continue manifest-driven development  
- maintain strict execution boundaries  
````
