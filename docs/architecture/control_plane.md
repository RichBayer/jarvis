# NeuroCore – Control Plane Architecture

---

# Purpose

The Control Plane governs all runtime behavior in NeuroCore.

It ensures that:

- all requests are classified before processing
- all actions are explicitly authorized
- no execution bypasses system authority
- system behavior remains controlled as capabilities expand
- all decisions are observable and traceable

---

# Core Principle

Nothing in NeuroCore executes outside the control plane.

All requests must pass through:

client → daemon → runtime manager → control plane → router → systems → model

---

# Architectural Role

The Control Plane is the authority layer inside the Runtime Manager.

It is responsible for:

- request classification
- mode selection
- capability authorization
- policy enforcement
- execution gating

The Runtime Manager orchestrates flow.

The Control Plane governs behavior.

---

# Responsibilities

The Control Plane is responsible for:

- validating all incoming requests
- classifying request type
- determining operating mode
- assigning allowed capabilities
- enforcing policy before downstream processing
- detecting execution intent
- denying or downgrading unsafe or unsupported actions
- enforcing context boundaries (especially for piped input)
- enforcing execution safety (confirmation model)
- emitting traceable decision events

---

# Request Model

All requests are converted into a structured internal form.

## Base Structure

```json
{
  "request_id": "...",
  "source": "cli_direct | cli_interactive | cli_pipe | internal",
  "input": "...",
  "normalized_input": "...",
  "request_class": "...",
  "mode": "...",
  "capabilities": [],
  "flags": {}
}
```

---

# Request Classes

## Conversational  
Natural language reasoning or explanation

## Knowledge  
Grounded retrieval-based requests

## External Input Analysis  
Piped or externally supplied data

## Execution Intent  
Requests that imply system action

## Runtime Admin  
Internal system queries and control

---

# Operating Modes

## Reasoning Mode  
Standard conversational behavior

## Analysis Mode  
Used for piped input and external data

## Execution Candidate Mode  
Execution intent detected but not yet approved

## Admin Mode  
Reserved for runtime control operations

---

# Capability Model

Each request is granted a limited set of capabilities.

## Capabilities

- REASON
- RETRIEVE
- USE_SESSION_MEMORY
- ANALYZE_EXTERNAL_INPUT
- REQUEST_EXECUTION
- ADMIN_RUNTIME

---

# Principle of Least Capability

Each request receives only the capabilities required.

Execution capability is tightly controlled and never implicitly granted.

---

# Piped Input Handling

Piped input (`| ai`) is treated as:

- source: cli_pipe
- mode: Analysis Mode
- capability: ANALYZE_EXTERNAL_INPUT

Rules:

- not executable
- isolated from normal conversation context
- not automatically stored in session memory
- interpreted only as data

---

# Execution Intent Handling

Requests that imply action are:

- classified as Execution Intent
- routed into execution flow
- governed by confirmation and policy enforcement

They are:

- blocked until confirmed (manual mode)
- allowed only through execution engine
- never executed directly by the model

---

# Confirmation-Based Execution

Execution is controlled through an explicit confirmation model.

Example:

Input:
"restart nginx"

System response:
confirmation required

Follow-up:
"confirm restart nginx"

Result:
execution allowed through execution engine

---

# Policy Enforcement Flow

1. request received  
2. classified by control plane  
3. mode selected  
4. capabilities assigned  
5. execution intent evaluated  
6. confirmation enforced (if required)  
7. authorized request emitted  
8. downstream system executes within constraints  

---

# Router Contract

The router must:

- operate only within granted capabilities
- not infer execution authority
- respect mode and request class

The router is not an authority layer.

---

# Runtime Manager Role

The Runtime Manager:

- receives request
- invokes control plane
- performs early validation (including ambiguity detection)
- forwards authorized request
- manages lifecycle and streaming

The Control Plane:

- governs all decisions

---

# Enforcement Rules

The Control Plane must ensure:

- no tool execution without authorization
- no model-triggered execution
- no router-side authority escalation
- no unvalidated memory writes
- no piped input treated as commands
- ambiguous queries are intercepted before processing
- all actions are observable
- all execution decisions are traceable

---

# Observability Integration (NEW)

The control plane is fully instrumented with tracing.

All major decision points emit structured trace events, including:

- execution detection
- confirmation checks
- tool resolution
- policy enforcement decisions

These events:

- share a single request_id across all system layers
- are written to structured logs
- provide full visibility into system behavior

This allows:

- verification of execution safety
- debugging of decision logic
- inspection of why requests were allowed or blocked

---

# Implementation Notes

The following behaviors are now implemented:

- Control Plane integrated into Runtime Manager
- Request classification enforced before routing
- Execution intent detected and routed through execution engine
- Confirmation-based execution model enforced
- Piped input isolated and treated as data only
- Ambiguous queries intercepted before transformation
- Full observability across all control plane decisions

Key enforcement point:

> Ambiguity detection occurs BEFORE any transformation or context injection

This prevents model-driven context fabrication.

---

# Outcome

A single, authoritative execution path that:

- prevents architectural drift
- enables safe expansion
- enforces execution safety
- provides full observability of decisions
- supports real tool execution

---

# Status

Phase 5A Design: COMPLETE  
Phase 5A Implementation: COMPLETE  
Phase 5H Observability Integration: COMPLETE  

---

# Next Step

Phase 5I – Real System Tools