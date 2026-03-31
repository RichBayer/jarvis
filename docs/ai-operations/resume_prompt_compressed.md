# NeuroCore Development – Compressed Resume Prompt

We are continuing development of my local AI system called NeuroCore.

NeuroCore was previously known as "Jarvis". References to Jarvis in file names, scripts, or documentation reflect earlier development stages.

---

# 🚨 CRITICAL OPERATING RULES (DO NOT BREAK)

* Do NOT guess system state, paths, or architecture
* If something is unclear → ASK before proceeding
* Always use real paths from this system
* Always provide copy/paste-ready commands
* Move one step at a time (no multi-step jumps)
* Explain WHY before implementation
* Validate each step before continuing
* Never assume code works—test it
* Never introduce temporary fixes that break architecture later

---

# 🧠 CURRENT SYSTEM STATE (CRITICAL)

NeuroCore is now a **persistent, stateful daemon-based AI system**

---

## ✅ COMPLETED CAPABILITIES

* UNIX socket daemon (`/tmp/neurocore.sock`)
* Runtime Manager (persistent processing layer)
* Router integrated into runtime
* Knowledge system refactored to lazy initialization
* Embedding model loads ONLY on first query
* Chroma vector DB persists across queries
* Full request → response pipeline operational
* Second query executes in ~3 seconds (no re-init)

---

## 🔥 KEY ARCHITECTURAL WIN (IMPORTANT)

Previously:

* knowledge system initialized at import time ❌

Now:

* knowledge system initializes ONLY on first query ✅
* system startup is instant ✅
* runtime controls initialization lifecycle ✅

---

# ⚠️ LESSONS LEARNED (DO NOT REPEAT THESE MISTAKES)

### 1. Python Module Execution

DO NOT run:

python runtime/neurocore_daemon.py ❌

ALWAYS run:

python -m runtime.neurocore_daemon ✅

Reason:

* ensures correct package resolution
* prevents import failures

---

### 2. Absolute Imports ONLY

All internal imports must be:

from scripts.query_knowledge import ...
from runtime.runtime_manager import ...

NEVER:

from query_knowledge import ... ❌

---

### 3. NO Heavy Initialization at Import

NEVER do this again:

embed_model = ...
chroma_client = ...
retriever = ...

at global scope ❌

Instead:

* wrap in class
* initialize lazily
* control from runtime manager

---

### 4. Persistent System Behavior

Expected behavior:

Startup:

* instant
* no model load

First query:

* initializes knowledge system

Second query:

* fast
* no reinitialization

---

# 🏗️ CURRENT ARCHITECTURE

Client
↓
UNIX Socket (/tmp/neurocore.sock)
↓
NeuroCore Daemon
↓
Runtime Manager (persistent state)
↓
Router (`jarvis_router.py`)
↓
KnowledgeBase (lazy-loaded)
↓
Chroma + Embeddings
↓
Ollama (LLM)

---

# 📁 PATHING RULES (CRITICAL)

Workspace root:

~/ai → /mnt/g/ai

Project root:

~/ai/projects/jarvis

ALWAYS use:

~/ai/...

NEVER default to:

/mnt/g/...

---

# 📁 KEY DIRECTORIES

* Runtime:
  ~/ai/projects/jarvis/runtime/

* Scripts:
  ~/ai/projects/jarvis/scripts/

* Build logs:
  ~/ai/projects/jarvis/build-logs/

* Screenshots:
  ~/ai/projects/jarvis/docs/screenshots/

* Knowledge DB:
  ~/ai/memory/chroma

---

# 🧪 EXECUTION RULES

Activate environment:

source ~/ai/runtime/python/jarvis-env/bin/activate

Shortcut available:

jarvisenv

Run daemon:

python -m runtime.neurocore_daemon

---

# 🧾 DOCUMENTATION RULES (MANDATORY)

Every milestone MUST include:

1. Build log
2. Screenshots
3. Embedded image markdown
4. Explanation of:

   * what was built
   * why it was built
   * issues encountered
   * how issues were resolved

---

# 📸 SCREENSHOT RULES

Screenshots must prove behavior:

1. Startup (no initialization)
2. First query (initialization)
3. Second query (fast path)

Naming format:

neurocore-<component>-<behavior>.png

---

# 📦 REQUIRED FILES FOR NEW SESSION

If context is missing, request these:

* System State File
* Home System Map
* Repository Map
* NeuroCore Vision Document

Located in:

docs/infrastructure/
docs/architecture/

DO NOT assume these are loaded

---

# 🧠 DEVELOPMENT STYLE

Act as a senior systems engineer.

* prioritize correct architecture over speed
* avoid temporary hacks
* maintain separation of concerns:

  * daemon = communication
  * runtime = state
  * router = logic
* verify before moving forward

---

# 🎯 CURRENT PHASE

Runtime Integration COMPLETE ✅

---

# 🚀 NEXT PHASE

CLI Interface Layer

---

# 🎯 NEXT OBJECTIVE

Replace manual socket interaction with CLI tool

Target usage:

ai "Explain SELinux"
df -h | ai
ai

---

# 🔧 NEXT IMPLEMENTATION TARGET

Create:

scripts/ai_cli.py

Responsibilities:

* connect to UNIX socket
* send structured request
* receive response
* support stdin piping

---

# 🧭 RESUME INSTRUCTION

Start with:

CLI interface design

Then implement:

scripts/ai_cli.py

Goal:

Natural command-line interaction with NeuroCore without manual Python socket usage.

