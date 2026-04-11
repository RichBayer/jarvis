# NeuroCore – Tool Execution Architecture

---

# Purpose

Defines how NeuroCore interacts with the system and environment through controlled execution.

---

# Core Principle

Tools are NOT shell commands.

Tools are structured capabilities.

---

# Tool Definition

Each tool must define:

- name
- description
- input schema
- output schema
- risk level
- approval requirement

---

# Example Tool

```json
{
  "name": "disk_usage",
  "input": {},
  "output": {
    "filesystem": "string",
    "usage_percent": "number"
  },
  "risk": "low",
  "approval": false
}
```

---

# Execution Flow

request  
→ control plane  
→ policy check  
→ tool selection  
→ execution engine  
→ result normalization  
→ response  

---

# Execution Rules

- no raw shell execution from model output
- all commands must be wrapped as tools
- outputs must be structured when possible
- errors must be captured and classified

---

# Existing Capability (IMPORTANT)

NeuroCore currently supports:

```bash
du -f | ai
```

This represents:

- first-stage input ingestion from CLI pipelines
- unstructured tool input (raw text stream)

---

# Interpretation

This is NOT yet a formal tool.

It is a transitional capability that:

- allows external command output to be processed
- bypasses structured tool definitions
- must eventually be absorbed into tool architecture

---

# Future Direction

Replace piping behavior with:

- formal tool ingestion interface
- structured parsing layer
- tool registration system

---

# Outcome

A controlled, extensible execution system that:

- prevents unsafe commands
- enables automation
- integrates cleanly with policy and control plane