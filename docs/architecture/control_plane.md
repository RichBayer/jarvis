# NeuroCore – Control Plane Architecture

---

# Purpose

The Control Plane governs all runtime behavior in NeuroCore.

It ensures that:

- all requests are classified before processing
- all actions are explicitly authorized
- no execution bypasses system authority
- system behavior remains controlled as capabilities expand

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

---

# Request Model (Phase 5A)

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
Execution intent detected but not allowed

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

Execution capability is never granted in Phase 5A.

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
- placed in Execution Candidate Mode
- NOT executed

They are:

- denied OR
- downgraded into advisory responses

---

# Deny vs Downgrade

## Deny  
Used when request is invalid or disallowed

## Downgrade  
Used when request is valid but unsupported

Example:

Input:  
"restart nginx"

Output:  
instructions for manual execution

---

# Policy Enforcement Flow

1. request received  
2. classified by control plane  
3. mode selected  
4. capabilities assigned  
5. policy applied  
6. authorized request emitted  
7. router executes within constraints  

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

---

# Implementation Notes (Phase 5A)

The following behaviors are now implemented:

- Control Plane integrated into Runtime Manager
- Request classification enforced before routing
- Piped input isolated and treated as data only
- Execution intent detected and downgraded
- Ambiguous queries intercepted using raw input
- Session memory influence controlled during validation

Key enforcement point:

> Ambiguity detection occurs BEFORE any transformation or context injection

This prevents model-driven context fabrication.

---

# Observability (Future Hook)

The control plane defines key decision points:

- request classification
- mode selection
- capability assignment
- execution denial

These will later be logged.

---

# Outcome

A single, authoritative execution path that:

- prevents architectural drift
- enables safe expansion
- prepares for tool execution
- enforces runtime governance

---

# Status

Phase 5A Design: COMPLETE  
Phase 5A Implementation: COMPLETE  

---

# Next Step

Phase 5B – Tool Execution Layer