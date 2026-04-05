# NeuroCore System Architecture

> NOTE:
> This system was originally named "Jarvis".
> It has since been renamed to "NeuroCore".
> References to "Jarvis" reflect the original name during development.

---

# Compute Node

Primary machine: Lenovo Legion Desktop

CPU: AMD Ryzen 7 5800X  
RAM: 32GB  
GPU: NVIDIA RTX 3060 12GB  
OS: Windows 11 with WSL2 Ubuntu  

NeuroCore currently runs primarily on this workstation.

The architecture is designed to support future distribution across multiple nodes.

---

# Storage Layout

Primary NVMe (G:)

G:\ai
- models
- runtime
- memory
- projects
- logs
- backups

External HDD (4TB)

- archive storage  
- camera recordings  
- AI memory archive  
- system backups  

All system state is filesystem-visible and portable.

---

# System Architecture (Layered)

NeuroCore is now a **context-aware, retrieval-grounded system** built as:

Interface Layer  
↓  
Transport Layer (Daemon + Socket)  
↓  
Runtime Layer  
↓  
Reasoning Layer (NEW)  
↓  
Logic Layer  
↓  
Knowledge Layer  
↓  
Model Layer  

---

# Interface Layer

Provides user interaction.

Current:

CLI  
[scripts/ai_cli.py](../../scripts/ai_cli.py)

Future:

Web UI (Open WebUI)  
Mobile devices (Tailscale)  
Voice nodes  
Tablet interfaces  

---

# Transport Layer

Components:

Daemon  
[runtime/neurocore_daemon.py](../../runtime/neurocore_daemon.py)

Socket:

/tmp/neurocore.sock  

Responsibilities:

Maintain persistent process  
Accept client connections  
Normalize requests  
Stream responses  

---

# Runtime Layer

File:

[runtime/runtime_manager.py](../../runtime/runtime_manager.py)

Responsibilities:

Coordinate system execution  
Route requests to logic layer  
Maintain runtime state  

---

# 🧠 Reasoning Layer (NEW)

This is the most important upgrade in the current system.

Components:

Session Memory  
Query Rewriting  

Files:

[scripts/session_memory.py](../../scripts/session_memory.py)  
[scripts/jarvis_router.py](../../scripts/jarvis_router.py)

---

## Session Memory

Storage:

/mnt/g/ai/memory/sessions/richard/session.json  

Responsibilities:

Store recent interactions  
Provide conversational context  
Enable multi-turn reasoning  

---

## Query Rewriting

Purpose:

Convert ambiguous follow-up questions into fully qualified technical queries.

Example:

"What column shows disk usage percentage?"

→

"What column in df -h output shows disk usage percentage?"

This ensures accurate retrieval.

---

# Logic Layer

File:

[scripts/jarvis_router.py](../../scripts/jarvis_router.py)

Responsibilities:

Interpret user intent  
Apply query rewriting  
Integrate memory context  
Build prompts  
Control LLM interaction  
Stream responses  

Key functions:

run_query()  
run_query_stream()  

---

# Knowledge Layer

File:

[scripts/query_knowledge.py](../../scripts/query_knowledge.py)

Core Components:

Chroma vector database  
Embedding model (MiniLM)  

Data Locations:

/mnt/g/ai/memory/knowledge  
/mnt/g/ai/memory/chroma  

---

## Knowledge System Capabilities

- Persistent vector storage  
- Metadata-based indexing  
- Command-aware retrieval (df, ps, etc.)  
- Fallback semantic search  

---

## 🔥 Metadata-Aware Retrieval (CRITICAL)

Retrieval is now constrained by detected command:

Example:

df query → only df documents  

This eliminates cross-command contamination.

---

## 🔥 Knowledge Normalization (CRITICAL)

Raw man pages are converted into structured operational knowledge.

Example:

Internal doc field:
pcent  

CLI output:
Use%  

System uses CLI-facing representation.

---

# Model Layer

Runtime:

Ollama (local LLM runtime)

Endpoint:

http://localhost:11434

Responsibilities:

Generate responses  
Provide streaming output  

---

# Streaming Pipeline

Ollama (streaming API)  
↓  
Router (generator)  
↓  
Daemon (socket streaming)  
↓  
CLI (real-time output)  

---

# Execution Flow (UPDATED)

1. User runs:

   ai "query"

2. CLI sends request via UNIX socket

3. Daemon:
   - receives request  
   - forwards to runtime manager  

4. Runtime Manager:
   - routes request to logic layer  

5. Reasoning Layer:
   - loads session memory  
   - rewrites query if needed  

6. Knowledge Layer:
   - detects command  
   - performs metadata-filtered retrieval  

7. Logic Layer:
   - builds prompt  
   - sends to Ollama  

8. Ollama streams response  

9. Response flow:

   Router → Daemon → CLI  

10. Memory updated

---

# Runtime Behavior

Cold Start:

Embedding model loads  
Vector DB initializes  
First query slower  

Warm State:

Fast responses  
No reinitialization  

---

# Memory Layer

Separate from knowledge.

Types:

Session memory (implemented)  
User memory (future)  
System memory (future)  

Memory is per-user isolated.

---

# Tool Execution Layer (NEXT)

This is the next major phase.

Capabilities to add:

Execute system commands  
Capture CLI output  
Analyze live system data  
Route queries between tools and LLM  

Example:

ai "check disk usage"

→ runs df -h  
→ analyzes output  

---

# Perception Layer (Future)

Inputs:

Microphones  
Cameras  
Sensors  
Smart devices  

---

# Automation Layer (Future)

Integration:

Home Assistant  
MQTT  

Controls:

Lights  
Sensors  
Cameras  
Rules  

---

# Distributed Architecture (Future)

Planned nodes:

AI compute node  
Knowledge node  
Automation node  
Interface nodes  

---

# Design Principles

Local-first computing  
Transparent filesystem state  
Modular architecture  
Persistent runtime  
Real-time streaming  
Deterministic retrieval  
Context-aware reasoning  

---

# Current Capabilities

Interactive CLI  
Streaming responses  
RAG (vector retrieval)  
Session memory  
Query rewriting  
Metadata-aware retrieval  
Knowledge normalization  

---

# Related Documentation

System Map  
[neurocore_system_map.txt](../infrastructure/neurocore_system_map.txt)

Repository Map  
[neurocore_repository_map.txt](../infrastructure/neurocore_repository_map.txt)

Resume Prompt  
[resume_prompt_compressed.md](../ai-operations/resume_prompt_compressed.md)

---

# Next Phase

Tool Execution Layer

---

# Design Goal

Centralized intelligence with distributed interaction points.

NeuroCore is evolving from:

information retrieval system  

to:

context-aware reasoning system  

next:

action-capable system