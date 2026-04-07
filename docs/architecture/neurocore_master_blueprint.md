# NeuroCore Master Blueprint

## 1. Purpose

NeuroCore is a local-first personal AI infrastructure system designed to operate as a persistent cognitive runtime rather than a stateless chatbot or simple application.

It is intended to provide:

- knowledge management
- software development assistance
- technical troubleshooting
- home infrastructure support
- daily life assistance
- long-term adaptive interaction for multiple users

NeuroCore must remain:

- local-first
- inspectable
- reproducible
- modular
- scalable
- human-controlled

---

## 2. System Identity

NeuroCore is not a chatbot.

NeuroCore is a persistent cognitive infrastructure system.

Its core design assumption is that intelligence should be centralized, stateful, and governed by a single runtime spine, while interfaces, tools, perception systems, and external services connect to that spine in a controlled way.

---

## 3. Governing Architectural Principles

### 3.1 Runtime-Centric Design
All interaction and all future environmental events must enter through the NeuroCore daemon and be governed by the Runtime Manager.

Nothing bypasses the runtime spine.

### 3.2 Local-First Operation
Core reasoning, memory, knowledge retrieval, and primary functionality must operate locally.

### 3.3 Filesystem-Visible State
Memory and system state should remain visible in the filesystem whenever possible.

### 3.4 Controlled Execution
NeuroCore must never directly execute arbitrary model-generated commands.

### 3.5 Human-Controlled Long-Term Memory
No silent accumulation of long-term memory.

### 3.6 Multi-User Isolation
Strict per-user memory separation.

### 3.7 Centralized Intelligence
Legion = brain  
R730 = infrastructure  
Nodes = interfaces

### 3.8 Phased Deployment Without Redesign
Architecture remains constant regardless of hardware stage.

---

## 4. High-Level System Model

- Cognitive Core (Legion)
- Infrastructure Core (R730)
- Edge Interaction Layer (Nodes)
- Perception Network (Sensors)

---

## 5. Logical Architecture

### 5.1 Interface Layer
CLI (current), UI, voice (future)

### 5.2 Transport Layer
UNIX socket → future network

### 5.3 Daemon Layer
runtime/neurocore_daemon.py

### 5.4 Runtime Manager
runtime/runtime_manager.py

### 5.5 Orchestration Layer
scripts/jarvis_router.py

Handles:
- intent
- rewriting
- routing
- grounding

---

### 5.6 Knowledge Layer

- scripts/query_knowledge.py
- Chroma
- metadata filtering
- grounded retrieval

---

### 5.7 Memory Layer

#### Session Memory (Short-Term)

Current implementation:

Session memory is stored per user at:

/mnt/g/ai/memory/sessions/<user>/session.json

Example (current system):
/mnt/g/ai/memory/sessions/richard/session.json

Managed by:
scripts/session_memory.py

Format:
- JSON
- rolling window of recent interactions

Purpose:
- query rewriting
- follow-up resolution
- conversational continuity

Session memory is stored outside the project repository to ensure:
- separation from version control
- local-first persistence
- easy backup and restoration
- multi-user scalability

---

#### Project Memory

Stored under:
/mnt/g/ai/projects/

User-controlled.

---

#### Personal Memory

- preferences
- personality
- tone

Stored only with approval.

---

#### Knowledge Memory

- indexed docs
- RAG

---

#### Future Working Memory

- active tasks

---

### 5.8 Model Layer

Ollama

---

### 5.9 Tool Execution Layer

Controlled Tool Registry

#### Tier 1 (Auto)
- read-only

#### Tier 2 (Approval)
- web / external

#### Tier 3 (Approval)
- mutating

Rules:
- no raw command execution
- structured outputs
- runtime-controlled

---

### 5.10 Perception Layer

Structured events only.

All inputs must be converted into structured events before entering NeuroCore.

---

### 5.11 Response Layer

- text
- audio
- UI
- actions

---

## 6. Current Runtime Pipeline

User  
→ CLI  
→ Socket  
→ Daemon  
→ Runtime Manager  
→ Router  
→ Session Memory  
→ Rewrite  
→ Retrieval  
→ Ollama  
→ Stream  
→ Memory Update

---

## 7. Physical Architecture

### Legion
- brain

### R730
- services

### Nodes
- input/output

### Sensors
- perception

---

## 8. Phase 1 Deployment

Everything runs on Legion  
Architecture unchanged

---

## 9. Memory Summary

Session → automatic  
Project → user-triggered  
Personal → suggestion + approval  
Knowledge → manual  

---

## 10. Tool Summary

Controlled execution  
Tiered permissions  
Approval system  

---

## 11. Perception Summary

Preprocessed structured events  
Unified ingestion  

---

## 12. Repo Mapping

runtime/  
scripts/  
memory/  
projects/  

---

## 13. Current Capabilities

- daemon
- streaming
- RAG
- metadata filtering
- session memory
- query rewriting
- grounded responses

---

## 14. Rules

### Forbidden
- bypass daemon
- raw command exec
- hidden memory
- split brain

### Required
- structured input
- controlled tools
- visible memory

---

## 15. Roadmap

Phase 5 next:
Tool Execution Layer

---

## 16. Immediate Next Step

Build:
- tool registry
- executor
- approval manager

---

## 17. Definition of Success

NeuroCore becomes:

- persistent
- local
- controlled
- scalable
- context-aware
- action-capable