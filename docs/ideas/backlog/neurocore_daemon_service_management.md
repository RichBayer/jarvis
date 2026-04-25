# Idea: NeuroCore Daemon Auto-Start + Service Management

---

## Notes

This should be implemented during:

Phase 6 – Distribution Layer

This MUST follow phase-aware development rules.

NOT during current tool expansion phase (Phase 5J).

---

## Metadata

- Status: Backlog  
- Priority: Medium  
- Category: Infrastructure / Distribution / Runtime  
- Origin: Development Discussion  
- Date: 2026-04-24  

---

## Summary

Implement system-level service management for the NeuroCore daemon so that it:

- starts automatically on system boot  
- runs continuously in the background  
- restarts automatically on failure  
- operates without manual user intervention  

This transitions NeuroCore from a manually launched process to a persistent runtime service suitable for real-world usage and distribution.

---

## Core Concept

NeuroCore is designed as a persistent daemon-based system.

This idea formalizes that design by integrating with the host operating system’s service manager.

For Ubuntu/Debian systems, this will use:

- systemd for service management  

---

## Problem This Solves

Current behavior:

- daemon must be started manually  
- daemon stops when session ends  
- not suitable for unattended or remote usage  
- adds friction for users  

This results in:

- inconsistent availability  
- poor user experience  
- non-production-ready behavior  

---

## Desired Outcome

After installation:

- NeuroCore daemon starts automatically at boot  
- daemon is always available for ACLI commands  
- no manual startup required  
- system behaves like a real service  

User experience:

```bash
acli "summary"

---

## Constraints

- MUST NOT introduce alternative execution paths outside daemon → control plane → execution engine flow
