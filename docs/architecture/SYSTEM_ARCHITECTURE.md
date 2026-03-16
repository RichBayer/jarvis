# Jarvis System Architecture

## Compute Node

Primary machine: Lenovo Legion Desktop

CPU: AMD Ryzen 7 5800X  
RAM: 32GB  
GPU: NVIDIA RTX 3060 12GB  
OS: Windows 11 with WSL2 Ubuntu

Jarvis currently runs primarily on this workstation.

Although the system is currently hosted on a single machine, the architecture is designed so that components may later be distributed across multiple nodes for scalability.

---

# Storage Layout

Primary NVMe (G:)

```
G:\ai
models
runtime
memory
projects
logs
backups
```

External HDD (4TB)

Archive storage  
camera recordings  
AI memory archive  
system backups  

This storage structure allows Jarvis data to remain visible and easily backed up.

---

# AI Runtime Layer

The runtime layer hosts the language models responsible for reasoning and response generation.

Runs inside WSL Ubuntu.

Core components:

Ollama – local model runtime  
Whisper – speech-to-text  
Piper – text-to-speech  

The runtime layer executes AI models and returns generated responses to the logic layer.

Future versions may support multiple models optimized for different tasks.

---

# Interface Layer

The interface layer provides ways for users to interact with Jarvis.

Examples include:

Open WebUI – browser-based interface  
CLI helper tools (such as `ai`)  
Mobile devices via Tailscale  
Tablets  
Voice nodes

The interface layer sends user requests to the logic layer.

---

# Logic Layer

The logic layer acts as the control system for Jarvis.

It receives requests from the interface layer and determines how the system should respond.

Responsibilities include:

Interpret user requests  
Determine system intent  
Select appropriate tools or data sources  
Assemble context for AI models  
Return responses to the interface layer

Possible routing targets include:

Knowledge retrieval  
System diagnostics  
Home automation commands  
Internet search  
External AI services

Conceptual request flow:

```
User request
↓
Intent detection
↓
Tool selection
↓
Data retrieval
↓
AI reasoning
↓
Response returned to interface
```

---

# Knowledge Layer

The knowledge layer allows Jarvis to retrieve and use information from local data sources rather than relying only on model training.

Core components:

Chroma – vector database for semantic embeddings  
LlamaIndex – document ingestion and retrieval framework

Responsibilities include:

Index local documents and notes  
Store semantic embeddings for retrieval  
Provide relevant context to the AI during queries

Typical knowledge sources include:

Personal documentation  
GitHub repositories  
System logs  
Technical notes  
Project files  

Conceptual workflow:

```
documents
↓
text chunking
↓
embedding generation
↓
vector database storage
↓
semantic retrieval
↓
context injected into AI prompt
```

This layer enables **retrieval augmented generation (RAG)**.

---

# Memory Layer

The memory layer stores contextual information generated through interaction with Jarvis.

This layer is separate from the knowledge system.

Memory types may include:

Conversation memory – summarized context from past interactions  
User memory – reminders, preferences, personal notes  
System memory – operational state or environment context

User memory must remain **isolated per user** so private information cannot be accessed by other users.

---

# Tool Execution Layer

The tool layer allows Jarvis to interact with external systems and perform actions beyond simple text responses.

Examples include:

System diagnostics tools  
Internet search tools  
Automation commands  
Development tools  
Log analysis utilities  

The logic layer determines when a tool should be used, and the tool layer executes the requested operation.

---

# Perception Layer

Sensors feeding data into the system may include:

Microphones  
Cameras  
Motion sensors  
Door sensors  
Smart devices

This layer allows Jarvis to perceive events occurring in the physical environment.

---

# Automation Layer

Home Assistant provides integration with household devices and automation systems.

Examples include:

Lights  
Cameras  
Sensors  
Automation rules

Communication occurs through MQTT or other automation protocols.

---

# Distributed Architecture (Future)

Although Jarvis currently runs primarily on one workstation, the architecture allows components to be distributed across multiple machines.

Possible future node roles include:

AI compute node – hosts language models and GPU workloads  
Knowledge node – stores vector databases and indexing systems  
Automation node – runs Home Assistant and device integrations  
Interface nodes – tablets, mobile devices, voice terminals

This distributed design allows Jarvis to scale as data size and system complexity increase.

---

# Design Goal

Centralized intelligence with distributed interaction points.

One powerful AI brain supported by specialized subsystems and lightweight terminals.