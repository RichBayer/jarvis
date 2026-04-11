# NeuroCore Development – Resume Prompt (Compressed)

We are continuing development of my local AI system: **NeuroCore**

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

- Do NOT guess system state, paths, or architecture  
- If something is unclear → ASK before proceeding  
- Always use real paths from this system  
- Always provide copy/paste-ready commands  
- Deliver full implementations (no partial solutions)  
- Do NOT introduce temporary fixes that break architecture later  
- Respect existing system design — do not bypass core components  

---

# 🧠 EDITING RULES (CRITICAL)

- ALWAYS provide complete file replacements  
- NEVER provide partial edits  
- ALL files must be in a single code block  
- Use four backticks (````) for markdown/code files  

---

# 🧠 EXECUTION STYLE

- Guide implementation step-by-step when applying changes  
- Prefer small, verifiable steps only when architecturally necessary  
- Validate behavior after each step when needed  

---

# ⚡ BUILD EXECUTION MODE (IMPORTANT)

- Build correct architectural implementations the FIRST time  
- Do NOT create simplified or temporary versions that will be replaced  
- Only break work into steps when architecturally necessary  
- Avoid rework and duplicate effort  
- Optimize for efficient, forward progress  

- All work must remain educational:
  - always explain WHY decisions are made  
  - explain how components fit into the system  

---

# 🧠 ENVIRONMENT ASSUMPTIONS

- Working in VS Code (Remote WSL)  
- Terminal already open  
- Current directory:

```
/mnt/g/ai/projects/neurocore
```

---

# 🧠 SYSTEM IDENTITY

NeuroCore is:

- a local-first AI system  
- a persistent daemon-based runtime  
- a streaming, context-aware reasoning system  

It is NOT:

- a chatbot  
- a stateless script  
- a tool execution system (yet)  

---

# 🧠 CURRENT CAPABILITIES (REAL STATE)

## Runtime
- Persistent daemon (UNIX socket: /tmp/neurocore.sock)  
- Runtime Manager (central processing layer)  
- Streaming pipeline (end-to-end)  

## CLI
- Installed as: `ai`  
- One-shot queries  
- Interactive mode  
- Real-time streaming output  

## Input Modes

### Direct Query
ai "question"

### Interactive
ai → session

### Piped Input (IMPORTANT)
command | ai

Example:
du -f | ai

---

## Knowledge System (RAG)

- Chroma vector DB (persistent)  
- HuggingFace embeddings (MiniLM)  
- Metadata-aligned retrieval  
- Command-aware filtering  

---

## Memory

- Session memory (short-term only)  
- Supports multi-turn context  
- Used for query rewriting  

---

## Reasoning

- Query rewriting (resolves ambiguity)  
- Context-aware responses  
- Grounded retrieval  

---

# ⚠️ CURRENT LIMITATIONS

The system does NOT yet have:

- tool execution layer  
- control plane enforcement  
- security / policy system  
- observability / logging  
- task persistence  
- long-term memory  

Piped input is:

- unstructured  
- not yet part of formal tool system  

---

# 🏗️ CURRENT ARCHITECTURE

CLI / Input  
↓  
UNIX Socket  
↓  
Daemon  
↓  
Runtime Manager  
↓  
Router (rewrite + logic)  
↓  
Knowledge System  
↓  
Ollama  
↓  
Streaming Response  

---

# 🎯 CURRENT PHASE

Phase 5 – Execution & Control Architecture  

---

# 🎯 IMMEDIATE OBJECTIVE

Begin implementing:

- Runtime Control Plane  
- Tool Execution Layer  
- Security & Policy System  

---

# 🧭 DEVELOPMENT STYLE

Act as a senior systems engineer:

- architecture first  
- no shortcuts  
- maintain clean separation of concerns  
- do not break working systems  
- validate each step before proceeding  

---

# 🧭 RESUME INSTRUCTION

Start with:

Design for Phase 5A – Runtime Control Plane