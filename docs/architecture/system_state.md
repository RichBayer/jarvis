# NeuroCore – System State

---

# Purpose

This document represents the **current implementation state of NeuroCore only**.

It defines:

- what exists
- how it behaves
- what is working
- what is NOT yet implemented

This document is used to guide development decisions.

If this document is incorrect, development decisions will be incorrect.

---

# System Identity

NeuroCore is a:

- local-first AI system
- persistent daemon-based runtime
- streaming, context-aware reasoning system

It is NOT:

- a stateless chatbot
- a request/response script
- a tool execution system (yet)

---

# Current Architecture

All interaction flows through:

CLI / Input  
↓  
UNIX Socket (/tmp/neurocore.sock)  
↓  
NeuroCore Daemon  
↓  
Runtime Manager  
↓  
Router (reasoning + rewriting)  
↓  
Knowledge System (RAG)  
↓  
LLM Runtime (Ollama)  
↓  
Streaming Response  

---

# Core Components

## Runtime Layer

- `runtime/neurocore_daemon.py`
- `runtime/runtime_manager.py`

Responsibilities:
- persistent process
- request handling
- streaming output

---

## Logic Layer

- `scripts/jarvis_router.py`

Responsibilities:
- query rewriting
- context handling
- routing decisions
- prompt construction

---

## Knowledge System

- `scripts/query_knowledge.py`
- Chroma (vector DB)
- HuggingFace embeddings (MiniLM)

Capabilities:
- semantic retrieval
- metadata-aligned filtering
- command-aware knowledge lookup

---

## Interface Layer

- `scripts/ai_cli.py`
- installed command: `ai`

Capabilities:
- one-shot queries
- interactive mode
- real-time streaming output

---

# Runtime Behavior

## Startup

- daemon starts instantly
- no heavy components loaded

---

## First Query (Cold Start)

- embedding model loads
- Chroma initializes
- retriever initializes

Behavior:
- slower response (~1–2 minutes)

---

## Warm State

- no reinitialization
- fast responses (~1–3 seconds)
- streaming active

---

# Input Capabilities

## Direct Query

```
ai "your query"
```

---

## Interactive Mode

```
ai
> query
> query
> exit
```

---

## Piped Input (IMPORTANT)

```
command | ai
```

Example:

```
du -f | ai
```

---

### Behavior

- CLI receives raw piped input
- forwards input to runtime
- model interprets output

---

### Current Status

- unstructured ingestion
- no schema
- no validation layer
- no tool abstraction

---

### Interpretation

This is an **early-stage execution interface**

It enables:

- command output analysis
- external data ingestion

It will later be replaced by:

- structured tool execution
- controlled input parsing
- policy-governed execution

---

# Memory System

## Session Memory

Location:

```
/mnt/g/ai/memory/sessions/richard/session.json
```

---

## Capabilities

- rolling conversation history
- multi-turn context
- supports query rewriting

---

## Limitations

- short-term only
- no long-term memory system
- no structured memory layers yet

---

# Reasoning Capabilities

## Query Rewriting

- resolves ambiguous follow-ups
- injects missing context

---

## Retrieval Control

- metadata filtering
- prevents cross-command contamination

---

## Response Behavior

- grounded in retrieved knowledge
- supports structured explanations

---

# Knowledge System Behavior

- lazy initialization
- persistent vector database
- optimized after first query

---

# Communication Model

- UNIX socket-based communication
- full request/response lifecycle
- streaming supported end-to-end

---

# Current Capabilities Summary

NeuroCore currently supports:

- persistent daemon runtime
- streaming responses
- CLI interface (`ai`)
- piped input ingestion (`| ai`)
- RAG-based knowledge retrieval
- metadata-aligned retrieval
- query rewriting
- session memory (short-term)

---

# Known Limitations

NeuroCore does NOT yet have:

- tool execution layer
- control plane enforcement
- security / policy system
- observability / logging system
- task persistence
- long-term memory
- structured execution model

---

# Current Phase

Phase 5 – Execution & Control Architecture

---

# Immediate Focus

- control plane (runtime authority)
- tool execution system
- security and policy enforcement

---

# Development Rules

- do not bypass daemon
- do not assume tools exist yet
- do not assume safe execution
- do not assume persistent tasks
- always validate behavior against runtime

---

# Maintenance

Update this document whenever:

- capabilities change
- architecture evolves
- major features are added

This document must always reflect **actual system behavior**.