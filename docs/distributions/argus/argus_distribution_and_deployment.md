# Argus ACLI – Distribution & Deployment Plan (V1)

---

## Purpose

This document defines how Argus ACLI will be packaged, distributed, and deployed as a usable product.

It establishes:

- how Argus is separated from NeuroCore (without breaking architecture)
- what components are included in the distribution
- how the runtime operates in a deployed environment
- how model (Ollama) integration is handled
- initial distro support strategy
- guiding principles to prevent architectural drift

This document is based on actual system implementation, not theory.

---

## Core Principle

Argus is NOT a standalone system.

Argus is:

A constrained distribution layer built on top of a bundled NeuroCore runtime.

NeuroCore remains:

- the execution engine
- the reasoning system
- the control authority

Argus provides:

- user-facing behavior
- system intelligence
- interpretation of system state

---

## System Model (Final)

User (ACLI)
    ↓
Argus CLI (acli)
    ↓
NeuroCore Daemon
    ↓
Runtime Manager
    ↓
Control Plane
    ↓

[Execution Path]
Execution Engine
    ↓
Argus Tool
    ↓
System Tool
    ↓
CommandRunner
    ↓
Operating System

[Reasoning Path]
Router
    ↓
Model (Ollama)

All execution MUST follow:

daemon → runtime_manager → control_plane → system

---

## What Argus Is

Argus ACLI is:

- a command-line interface (acli)
- a distribution layer on top of NeuroCore
- a system intelligence tool
- a read-only diagnostic system

Argus provides:

- system inspection
- structured diagnostics
- raw evidence for verification
- recommended next steps
- optional AI explanation layer
- planned persistent resolved issue memory and recurrence awareness

---

## What Argus Is NOT

Argus does NOT:

- execute commands directly
- bypass the control plane
- modify system state (V1)
- operate independently of NeuroCore
- rely on external APIs or cloud systems

---

## Distribution Composition

Argus V1 includes:

### 1. CLI Interface

acli command

- primary user entry point
- wraps NeuroCore CLI behavior
- sends structured requests over UNIX socket

---

### 2. Argus Tool Layer

tools/argus/

Implemented diagnostic tools:

- system_summary
- process_top_analysis
- memory_analysis
- disk_analysis
- network_analysis
- connections_analysis
- uptime_analysis
- logs_analysis
- system_analysis

Responsibilities:

- aggregate system signals
- interpret structured data
- produce findings + recommendations
- preserve raw evidence for verification
- surface recurrence insights from incident memory when that system is implemented

---

### 3. System Tool Layer

tools/system/

- performs all system interaction
- uses CommandRunner
- returns structured data
- preserves raw command output for downstream evidence

---

### 4. Minimal NeuroCore Runtime

Required components:

runtime/
tools/base_tool.py
tools/execution_engine.py
tools/tool_registry.py
tools/system/command_runner.py

Responsibilities:

- enforce execution rules
- manage request lifecycle
- maintain system safety
- preserve observability

---

### 5. Distribution Config

distributions/argus/

Includes:

- tool manifest
- personality definition
- future config options

---

### 6. Model Integration (Ollama)

Local model runtime for reasoning.

---

### 7. Incident Memory System (V1 Planned)

A structured, deterministic incident memory system is planned for V1.

Purpose:

- persist resolved issues (with user approval)
- detect recurring faults
- provide system-specific historical awareness

Storage:

~/.argus/incidents/

Format:

- JSON
- one file per incident
- human-readable and portable

Behavior:

- Argus tools generate structured incident candidates during diagnostics
- user is prompted to save resolved incidents
- recurrence detection is performed using deterministic matching
- recurrence insights are surfaced during future diagnostics

Example output:

“This nginx failure has occurred 3 times in the past 14 days.”

Key Principles:

- this is NOT AI memory
- no model dependency
- no system state modification
- no automated fixes
- operates entirely within Argus read-only model

Implementation status:

- incident memory integration points are defined
- full incident memory implementation is not yet complete
- implementation must remain phase-aligned and must not interrupt primary output-control work unless explicitly selected as the active task

---

## ACLI Command Model

Primary command:

acli "summary"

Examples:

acli "summary"
acli "processes"
acli "logs ssh"
acli "network"
acli "what is wrong with nginx?"

Design goals:

- simple
- consistent
- natural language compatible
- fully routed through NeuroCore

---

## Model Strategy (Ollama Integration)

Argus V1 supports model-assisted reasoning.

Model is used for:

- explanation
- follow-up questions
- contextual reasoning
- log interpretation

Model is NOT required for:

- core diagnostics
- system inspection
- structured findings
- raw evidence preservation

---

## Install Tiers (Planned)

### Tier 1 — Core

No model or very small model (1–3B)

- system tools + Argus tools only
- deterministic diagnostics
- structured findings
- raw evidence for verification
- lightweight and fast

---

### Tier 2 — Standard (Default)

7B model (recommended)

- full Argus experience
- explanation + reasoning
- best balance of performance and capability

---

### Tier 3 — Pro

13B+ model

- advanced reasoning
- improved interpretation
- future training capabilities

---

## Model Detection (Installer Behavior)

Installer should detect:

- CPU
- RAM
- GPU / VRAM
- disk space

Then recommend install tier.

---

## Degraded Operation

If model is unavailable:

- Argus tools still function
- diagnostics still work
- findings and recommendations still work
- raw evidence remains available for verification
- system remains usable

Model enhances system, but does not define it.

---

## Distro Support Strategy

### V1 Support

Ubuntu / Debian (systemd-based)

---

### V2 Expansion

Rocky Linux / RHEL / Fedora

---

## Critical Insight

Argus portability is achieved through:

System Tool Layer abstraction

---

## What Changes Across Distros

Only:

tools/system/

---

## What Does NOT Change

runtime/
control_plane
execution_engine
argus tools

---

## Execution Safety Rules

Must always enforce:

- no execution without control plane
- no direct system access from Argus tools
- no subprocess outside CommandRunner
- full trace observability

---

## Final Principle

Argus is not a chatbot.

Argus is a system that inspects real environments
and uses structured intelligence to explain them.

---

## End State Goal

A local-first system intelligence platform
that understands system state
and evolves toward long-term operational awareness.