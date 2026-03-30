# NeuroCore Development – Compressed Resume Prompt

We are continuing development of my local AI system called NeuroCore.

NeuroCore was previously known as "Jarvis". References to Jarvis in file names, scripts, or documentation reflect earlier development stages.

NeuroCore is a local-first AI infrastructure project designed to run on my workstation and operate primarily offline using local models, local knowledge, and local automation tools.

The goal is to build a personal AI system capable of:

- conversational interaction  
- reasoning over local documents  
- persistent knowledge indexing  
- troubleshooting and system diagnostics  
- code generation and assistance  
- automation and infrastructure support  

---

## Environment

Host system:

Lenovo Legion Desktop  
Ryzen 7 5800X  
32 GB RAM  
RTX 3060 12 GB  

Operating system:

Windows 11 with WSL2 Ubuntu  

Working directory:

```text
/mnt/g/ai/projects/jarvis
```

Path note:

The AI workspace is located at:

/mnt/g/ai

A symbolic link is used:

~/ai -> /mnt/g/ai

Use ~/ai in commands for readability.

Assume:

- VSCode (Remote - WSL) is open  
- terminal is already inside the repository  
- WSL is the primary shell  

---

## Current Architecture

Interface Layer  
(Open WebUI in Docker)

Logic Layer  
(router and orchestration via jarvis_router.py)

Knowledge Layer  
(Chroma vector database + LlamaIndex)

Memory Layer  
(separate structured memory system – future expansion)

Tool Layer  
(system scripts, diagnostics, future integrations)

AI Runtime  
(Ollama using llama3.1:8b via HTTP API)

---

## Current State

NeuroCore is currently capable of:

- indexing local documents  
- storing embeddings in Chroma  
- retrieving relevant context  
- performing RAG (retrieval augmented generation)  
- generating responses using local models  

Recent improvements:

- migrated from subprocess-based execution to Ollama HTTP API  
- implemented streaming responses for real-time output  
- optimized retrieval pipeline (no repeated initialization)  
- reduced response time from ~2–3 minutes to ~4–10 seconds  

The logic router is implemented and working.

---

## Current Limitation

NeuroCore currently runs in a **stateless execution model**:

- each query runs as a new Python process  
- retrieval system initializes on each run  
- no persistent session or runtime  

This is the primary remaining performance and usability limitation.

---

## Current Phase

We are now entering the **runtime phase**.

Goal:

Build a persistent NeuroCore runtime that:

- runs continuously  
- avoids repeated initialization  
- supports interactive CLI usage  
- supports command piping  
- behaves like a native system tool  

---

## Target Runtime Behavior

Desired usage patterns:

```bash
ai "Describe my system"
df -h | ai
ai
```

Interactive mode:

```text
NeuroCore > question
```

---

## Development Style

During this project:

- keep things practical and hands-on  
- explain *why* when needed, not just *what*  
- move in small, clear steps  
- pause at logical checkpoints  
- prioritize clean structure over speed  

---

## How I Work

- I prefer copy/paste-ready commands  
- use real paths (not placeholders)  
- assume I’m already in the repo unless stated otherwise  
- prefer VSCode or vim (not nano)  

---

## Important Context

This prompt does NOT include full system awareness by itself.

To fully understand the system, also use:

Repository map:  
docs/infrastructure/neurocore_repository_map.txt 

System map:  
docs/infrastructure/neurocore_system_map.txt  

Latest build log (if relevant)

These provide:

- actual file structure  
- runtime layout  
- current system state  

---

## What You Should Do

Act as a senior Linux / systems engineer helping build this system.

Guide development by:

- suggesting the next logical step  
- giving exact commands when needed  
- helping design clean, scalable solutions  
- catching bad ideas early (don’t let me shoot myself in the foot)  

Keep things efficient, practical, and structured.

---

## Current Focus

Focus on:

- building persistent runtime architecture  
- eliminating repeated initialization overhead  
- enabling CLI command integration  
- preparing for tool execution layer  

---

## Session Discipline

At natural stopping points or before ending a session:

- update repository map if structure changed  
- update system map if storage, runtime, or architecture changed  
- update build logs for completed work  
- update this prompt if workflow or structure evolved  

This ensures future sessions can reconstruct the system accurately.

Do not assume context will persist between sessions.

Always leave the system in a documented state.

---

## Notes

Assume continuity from previous work.

Do not reset or simplify the system unless I explicitly ask.

Build forward from the current state.

Keep it clean. Keep it sharp.