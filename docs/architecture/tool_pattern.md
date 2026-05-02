# NeuroCore – Tool Pattern (Ground Truth)

---

# Purpose

This document defines how tools ACTUALLY work in NeuroCore.

This is not a theoretical design.

This is based on:

- BaseTool implementation
- system_info tool (first real tool)
- execution engine behavior
- real build results and failures
- structured system tool normalization
- Argus diagnostic tool implementation

This document exists so future tools are built consistently and correctly.

---

# Core Principle

Tools do NOT define execution behavior.

NeuroCore does.

Tools are:

> Controlled execution units that run inside the system

All tools must follow the same lifecycle and structure.

---

# Execution Flow (REAL)

All tool execution follows this exact path:

control_plane  
→ execution_engine  
→ tool.validate_request()  
→ tool.execute()  
→ build_result()  
→ runtime  
→ CLI  

Tools are never called directly by:

- CLI
- router
- model
- external input

---

# Tool Structure (REQUIRED)

Every tool must define:

- name
- description
- input_schema
- execution_mode

From BaseTool:

```
name: str
description: str
input_schema: Dict
execution_mode: "auto" | "manual" | "dry-run"
```

---

# Input Model

All tools receive a full request object:

```
{
  "tool": "...",
  "input": {...},
  "trace": {...}
}
```

Tools must:

- extract from request["input"]
- NOT modify request structure
- NOT generate new trace context

---

# Validation Model

Validation is enforced BEFORE execution:

execution_engine → tool.validate_request()

BaseTool handles:

- required field validation
- input type validation
- schema enforcement

Each tool must implement:

```
def validate_input(self, tool_input)
```

---

# Execution Pattern (MANDATORY)

All tools must follow this pattern inside execute():

---

## 1. Extract Context

```
ctx = trace_context_from_request(request)
tool_input = request["input"]
```

---

## 2. Emit Invocation Trace

```
trace_event(
    event="tool_invoked",
    context=ctx,
    component="<tool_name>",
    details={"input": tool_input}
)
```

---

## 3. Perform Execution Logic

System tools:

- Use CommandRunner for ALL system interaction
- No direct subprocess usage
- No external execution paths

Example:

```
CommandRunner.run([...])
```

Argus tools:

- MUST NOT call CommandRunner
- MUST NOT execute subprocess directly
- MUST use system tools as their data source
- MUST consume structured system tool data

---

## 4. Emit Completion Trace

```
trace_event(
    event="<tool_name>_execution_completed",
    context=ctx,
    component="<tool_name>",
    status="success"
)
```

---

## 5. Return Result

ALL tools must return using:

```
return self.build_result(
    status="success",
    message="<formatted output>",
    data={...}
)
```

---

# Command Execution Rule (CRITICAL)

ALL system interaction must go through:

tools/system/command_runner.py

System tools must NEVER:

- import subprocess
- execute shell commands directly
- bypass CommandRunner

Argus tools must NEVER:

- call CommandRunner
- execute subprocess directly
- bypass system tools for data collection

---

# Output Contract (REAL)

All tools return:

```
{
  "status": "success" | "error",
  "tool": "<tool_name>",
  "message": "<human readable output>",
  "data": {...}
}
```

The `data` field is required.

System tools use `data` for structured system state and preserved raw command output.

Argus tools use `data` for interpreted diagnostics and raw evidence.

---

## System Tool Data Pattern

System tools return structured machine-usable data.

They must preserve raw command output when available.

Example:

```
{
  "status": "success",
  "tool": "<system_tool>",
  "message": "...",
  "data": {
    "<structured_fields>": "...",
    "raw": {
      "stdout": "...",
      "stderr": "...",
      "returncode": 0
    }
  }
}
```

---

## Argus Tool Data Pattern

Implemented Argus diagnostic tools return interpreted data plus raw evidence.

Example:

```
{
  "status": "success",
  "tool": "<argus_tool>",
  "message": "...",
  "data": {
    "severity": "OK | INFO | WARN | CRITICAL",
    "findings": [...],
    "recommendations": [...],
    "raw": { ... }
  }
}
```

Argus tools must derive interpretation from structured data, not formatted message output.

Raw evidence is preserved for verification and future grounding.

---

## IMPORTANT

The CLI uses:

- status
- message
- data

Tools must ensure:

> message is readable and formatted

Structured diagnostic display should rely on `data`, not message parsing.

---

# Formatting Rule

Tools are responsible for producing clean human-readable summaries.

The CLI / ACLI is responsible for presenting structured diagnostic sections.

This was validated during system_info and Argus diagnostic tool builds:

- CLI expects clean message output
- tools must NOT include duplicate status markers (ex: [OK])
- Argus diagnostic output must preserve structured data for display
- raw evidence must be preserved without replacing interpretation

---

# Execution Modes

## auto

- executes immediately
- used for read-only tools

## manual

- requires confirmation
- enforced by control plane

## dry-run

- does not execute
- returns advisory output only

---

# Trace Integration

All tools must:

- use existing trace context
- emit trace events
- NOT generate new request IDs

Trace must remain continuous across:

execution_engine → tool → command_runner

For Argus tools, trace continuity must remain intact across:

execution_engine → argus_tool → system_tool → command_runner

---

# What Tools MUST NOT Do

Tools must NOT:

- bypass execution engine
- modify system state (in current phase)
- create new execution paths
- return raw unformatted command output as a replacement for interpretation
- depend on CLI formatting
- assume routing behavior

Argus tools must additionally NOT:

- call CommandRunner directly
- parse formatted message output for diagnostic logic
- duplicate system tool execution logic

---

# What Tools ARE Responsible For

Tools ARE responsible for:

- validating input
- executing controlled commands when they are system tools
- consuming structured system data when they are Argus tools
- formatting output clearly
- emitting trace events
- returning structured results
- preserving raw evidence when available

---

# system_info – Reference Implementation

system_info is the first real tool and defines the original working pattern.

Key behaviors:

- uses trace_context_from_request()
- emits trace_event lifecycle
- validates structured input
- uses CommandRunner exclusively
- formats output internally
- returns via build_result()

All future system tools must follow this model.

---

# Argus Diagnostic Tools – Reference Pattern

The implemented Argus diagnostic tools define the current diagnostic pattern.

Key behaviors:

- inherit from BaseTool
- receive full request object
- use trace_context_from_request()
- emit trace_event lifecycle
- call system tools through the registry
- consume structured system tool `data`
- produce deterministic findings
- assign severity
- return recommendations
- preserve raw evidence under `data["raw"]`

Implemented examples include:

- `disk_analysis`
- `memory_analysis`
- `network_analysis`
- `process_top_analysis`
- `connections_analysis`
- `uptime_analysis`
- `logs_analysis`
- `system_summary`
- `system_analysis`

All future Argus tools must follow this model.

---

# Key Lessons from Real Build

From Phase 019:

- Control plane must explicitly map execution triggers
- Daemon serialization must be correct (JSON boundary is critical)
- CLI must remain simple
- Tools must NOT format for CLI incorrectly
- Output must be clean, not duplicated

From later tool-layer phases:

- Structured data must survive the full pipeline
- Argus tools must consume structured data, not formatted messages
- Raw evidence must be preserved for verification
- CLI / ACLI presentation must not replace tool-layer diagnostic logic

---

# Contract vs Behavior (IMPORTANT)

The tool contract is fixed across all tools.

What changes between tools is:

- execution_mode (auto / manual / dry-run)
- level of validation
- whether system state is modified
- whether the tool is a system tool or an Argus tool
- the shape of structured diagnostic data

The execution lifecycle does NOT change.

This ensures:

- consistent system behavior
- predictable execution flow
- safe expansion into more powerful tools

---

# Final Rule

If a tool does not match this pattern:

It is incorrect.

---

# Purpose Going Forward

This document ensures:

- consistent tool behavior
- clean expansion of system capabilities
- stable foundation for Argus
- preservation of raw evidence without breaking deterministic interpretation

All future tools must follow this pattern exactly.