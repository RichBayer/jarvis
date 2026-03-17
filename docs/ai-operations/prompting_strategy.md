# Jarvis Prompting Strategy

## Purpose

This document explains how I structure prompts when working with ChatGPT during the development of Jarvis.

The goal is simple:

- pick up where I left off without confusion  
- avoid re-explaining the system every time  
- get accurate, copy/paste-ready commands  
- keep development consistent over time  

This isn’t just convenience — this is part of how Jarvis is being built.

---

## Core Idea

The prompt is used to **rebuild system awareness**.

Instead of relying on long chat history, I give ChatGPT just enough structured information to understand:

- how Jarvis is designed  
- where everything lives  
- what phase I’m in  
- how I want to work  

---

## Working Environment

Assume the following unless I say otherwise:

- I’m in VSCode (Remote - WSL)
- Terminal is already open inside the repo
- Current working directory:

```text
/mnt/g/ai/projects/jarvis
```

- WSL Ubuntu is the main shell

PowerShell is available if needed, but WSL + VSCode is home base.

---

## Prompt Types

### Full Resume Prompt

Used when I need to fully rebuild context.

Examples:

- starting a fresh thread  
- making architecture changes  
- after a long break  

This includes everything:
architecture, philosophy, build history, etc.

---

### Compressed Resume Prompt

Used for normal day-to-day work.

This is faster and lighter, but still gives enough context to keep moving.

⚠️ Important:  
The compressed prompt **does not include filesystem awareness** by itself.

---

## Required Context (This Is the Key)

To actually understand the system properly, ChatGPT also needs:

- Repository map  
- System map  
- Latest build log (if I’ve made recent changes)  

### Current Files

Repository map:  
[docs/infrastructure/jarvis_repository_map.txt](../infrastructure/jarvis_repository_map.txt)

System map:  
[docs/infrastructure/jarvis_system_map.txt](../infrastructure/jarvis_system_map.txt)

These always point to the **latest version** of the system.

I don’t version these manually — I just update them and Git tracks the history.

---

## What Each Piece Does

### Prompt
Gives:
- architecture
- current phase
- workflow rules
- how I like to work

### Repository Map
Shows:
- repo structure
- scripts
- docs
- what already exists

### System Map
Shows:
- AI workspace layout
- storage locations
- knowledge + backup structure
- where Jarvis actually lives

### Build Log
Shows:
- what I just did
- what changed
- anything that broke and got fixed

---

## How I Start a Session

When using the compressed approach:

1. Paste compressed prompt  
2. Provide repository map  
3. Provide system map  
4. Provide latest build log (if needed)  

That gives ChatGPT enough to work like it’s inside my system.

---

## How I Want Responses

### Commands

- Always copy/paste ready  
- Use real paths  
- Prefer full paths when it matters  
- No placeholders unless absolutely necessary  

### Tools

- Prefer VSCode or vim  
- Avoid nano  

### Style

- Keep it clear and practical  
- Don’t over-explain  
- Stay focused on getting things working  
- Move in small steps  

---

## Why This Matters

Without this structure:

- things get inconsistent fast  
- paths get guessed wrong  
- I waste time re-explaining everything  

With this:

- I can jump back in instantly  
- commands are accurate  
- progress stays clean and documented  

---

## Where This Is Going

Eventually this gets replaced by a single file:

```text
docs/infrastructure/jarvis_system_state.md
```

That file will include everything:

- filesystem layout  
- running components  
- models  
- storage  
- architecture  

At that point I’ll only need:

- compressed prompt  
- system state file  
- latest build log  

---

## Long-Term Goal

Jarvis should eventually be able to:

- understand its own structure  
- read its own docs  
- guide its own setup  
- continue its own build process  

---

## Summary

This prompt system is how I keep:

- context consistent  
- commands accurate  
- development efficient  

It’s basically the bridge between me and the system.