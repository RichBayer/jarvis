# NeuroCore Development – Compressed Resume Prompt

We are continuing development of my local AI system called NeuroCore.

NeuroCore was previously known as "Jarvis". References to Jarvis in file names, scripts, or documentation reflect earlier development stages.

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

* Do NOT guess system state, paths, or architecture
* If something is unclear → ASK before proceeding
* Always use real paths from this system
* Always provide copy/paste-ready commands
* Deliver full production-quality implementations (no toy or partial builds)
* Execution should be guided step-by-step when applying changes (one command at a time when needed)
* Prioritize clean, complete solutions over incremental or temporary approaches
* Never introduce temporary fixes that break architecture later
* Assume system is evolving toward production-grade architecture, not experimentation

---

# 🧠 CURRENT SYSTEM STATE (CRITICAL)

NeuroCore is now a persistent, streaming, daemon-based AI system with an interactive CLI

---

## ✅ COMPLETED CAPABILITIES

* UNIX socket daemon (/tmp/neurocore.sock)
* Runtime Manager (persistent processing layer)
* Router integrated into runtime
* Knowledge system with lazy initialization
* Chroma vector DB persistence
* CLI interface installed as system command (ai)
* Interactive CLI mode (multi-query session)
* Streaming response pipeline (end-to-end)

---

## 🔥 MAJOR ARCHITECTURAL WIN (STREAMING PIPELINE)

Streaming is now implemented across the entire system:

Ollama (streaming API)  
↓  
Router (generator-based streaming)  
↓  
Daemon (chunk forwarding over socket)  
↓  
CLI (real-time output)

This enables:

* real-time responses
* improved UX
* foundation for API + UI streaming
* future voice integration

---

## 🔥 CLI CAPABILITIES

NeuroCore CLI now supports:

One-shot mode:
ai "your query"

Interactive mode:
ai
> query
> query
> exit

Exit methods:

* exit / quit
* CTRL + C
* CTRL + D

---

## ⚠️ LESSONS LEARNED

1. Streaming must originate at source  
Do NOT print inside router  
Use generators → propagate through system  

2. CLI naming conflicts  
Shell functions can override binaries  
Always verify with: type ai  

3. Silent failures in streaming  
If no chunks appear:  
* verify generator output  
* inspect daemon streaming loop  

4. Clean separation of concerns  
* Router = data generation  
* Daemon = transport  
* CLI = interface  

---

# 🏗️ CURRENT ARCHITECTURE

CLI (ai)  
↓  
UNIX Socket (/tmp/neurocore.sock)  
↓  
NeuroCore Daemon  
↓  
Runtime Manager  
↓  
Router (run_query / run_query_stream)  
↓  
KnowledgeBase (lazy-loaded)  
↓  
Chroma + Embeddings  
↓  
Ollama (LLM)  

---

# 📁 PATHING RULES

Workspace root:  
~/ai  

Project root:  
~/ai/projects/jarvis  

---

# 🎯 CURRENT PHASE

Streaming + Interactive CLI COMPLETE

---

# 🚀 NEXT PHASE

CLI Enhancement + System Integration

---

# 🎯 NEXT OBJECTIVES

1. STDIN ingestion  
df -h | ai  
cat logs.txt | ai  

2. Session memory (multi-turn context)

3. Tool execution integration

---

# 🧭 DEVELOPMENT STYLE

Act as a senior systems engineer.

* architecture first  
* no shortcuts  
* full implementations over partial edits  
* validate after each change  
* maintain clean separation of concerns  

---

# 🧭 RESUME INSTRUCTION

Start with:

STDIN ingestion design and implementation