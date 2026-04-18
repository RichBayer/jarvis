# NeuroCore – Tool Execution Architecture

---

# Purpose

The Tool Execution layer is responsible for performing controlled system actions inside NeuroCore.

It ensures that:

- all execution flows through a single controlled path
- no component executes system actions directly
- execution is validated, authorized, and observable
- system safety is enforced at all times

---

# Core Principle

All execution must pass through the execution engine.

No tool is called directly by:

- the router
- the model
- the CLI
- any external input

Execution flow is strictly enforced.

---

# Execution Flow

All execution follows this path:

```
client
→ daemon
→ runtime manager
→ control plane
→ execution engine
→ tool
→ execution engine
→ control plane
→ runtime manager
```

---

# Architectural Role

The Tool Execution layer consists of:

- Execution Engine (orchestration)
- Tool Registry (tool discovery)
- BaseTool contract (standard interface)
- Tools (implementation layer)

---

# Execution Engine

Location:

```
tools/execution_engine.py
```

Responsibilities:

- receive authorized execution requests from control plane
- resolve the correct tool from registry
- validate tool input
- invoke tool execution
- return structured results
- propagate trace context

The execution engine is the ONLY component allowed to invoke tools.

---

# Tool Registry

Location:

```
tools/tool_registry.py
```

Responsibilities:

- maintain list of available tools
- resolve tools by name
- enforce controlled tool availability

---

# BaseTool Contract

Location:

```
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

# Tool Interface (UPDATED)

Tools no longer receive only input.

They now receive the full execution request.

## Previous Model (deprecated)

```
tool.execute(input)
```

## Current Model

```
tool.execute(request)
```

---

# Request Structure Passed to Tools

Tools receive a structured request:

```json
{
  "tool": "...",
  "input": {
    "action": "...",
    "service": "..."
  },
  "trace": {
    "request_id": "...",
    "source": "...",
    "metadata": {}
  }
}
```

---

# Why This Change Matters

Passing the full request enables:

- trace context propagation (request_id continuity)
- full observability inside tools
- consistent execution behavior across all layers

Without this:

- tools generate new request_ids
- trace continuity breaks
- system becomes harder to debug

---

# Tool Responsibilities

Each tool must:

- validate input using BaseTool contract
- extract required data from request["input"]
- NOT modify trace context
- emit trace events using provided context
- return structured results

Tools must NOT:

- generate new request_ids
- bypass execution engine
- perform unauthorized actions

---

# Execution Modes

Each tool defines an execution mode:

## auto
- executes immediately

## manual
- requires confirmation before execution

## dry-run
- never executes
- returns advisory response only

---

# Confirmation Model

For manual tools:

1. user issues command  
2. control plane detects execution intent  
3. execution is blocked  
4. confirmation required  
5. user confirms  
6. execution engine proceeds  

---

# Safety Model

The execution system enforces:

- no execution without control plane approval
- no direct execution from model or router
- no execution from piped input
- no bypass of confirmation model
- strict tool validation before execution

---

# Observability Integration (NEW)

Execution is fully traceable.

Each step emits structured trace events:

- execution detection
- tool resolution
- validation
- execution start
- execution completion

All events:

- share the same request_id
- are logged centrally
- allow full request lifecycle inspection

---

# Example Execution Trace

```
runtime_manager → execution detected
control_plane   → confirmation required
control_plane   → execution allowed
execution_engine → execution started
execution_engine → tool resolved
execution_engine → validation passed
service_manager  → tool invoked
service_manager  → execution simulated
execution_engine → execution completed
```

---

# Current Tool (Phase 5H)

## service_manager

Capabilities:

- start
- stop
- restart
- status

Current behavior:

- simulated execution
- full trace support
- confirmation-based execution

---

# Outcome

The tool execution system now provides:

- controlled execution flow
- strict safety enforcement
- standardized tool interface
- full trace visibility
- architecture ready for real system tools

---

# Status

Execution Engine: COMPLETE  
Tool Contract: COMPLETE  
Trace Integration: COMPLETE  

---

# Next Step

Replace simulated tools with real read-only system tools