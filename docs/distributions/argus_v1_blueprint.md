````markdown
# Argus V1 – Tooling & Capability Blueprint

---

# Purpose

This document defines:

- the complete Argus V1 tool set  
- capability scope and constraints  
- command-level mapping (via system tools)  
- dependency handling model  
- Argus tool architecture pattern  

This document ensures Argus V1 delivers high value while remaining simple, reliable, and safe.

---

# System Definition (V1)

Argus V1 is:

A read-only system intelligence layer built on top of NeuroCore.

Argus operates entirely within the NeuroCore execution pipeline and does not introduce new execution paths.

Argus V1 MUST:

- use real system data  
- consume structured system tool output (`data`)  
- provide actionable insight  
- remain read-only  
- operate through controlled execution only  

---

# Core Design Rules

## 1. Read-Only Enforcement

Argus must NEVER:

- modify files  
- restart services  
- change system configuration  
- execute destructive actions  

---

## 2. Execution Boundary

Argus tools:

- MUST NOT call CommandRunner  
- MUST NOT execute system commands directly  
- MUST use system tools exclusively  

All execution remains:

```
control_plane → execution_engine → system_tool → command_runner
```

Argus sits above this layer.

---

## 3. Structured Data Requirement (CRITICAL)

All Argus tools depend on system tools returning:

```
{
  "status": "...",
  "message": "...",
  "data": { ... }
}
```

Argus tools MUST:

- consume `data`  
- ignore formatted message output  
- avoid regex-based parsing  

---

## 4. Local Execution Only

- no external APIs  
- no telemetry  
- no cloud dependencies  

---

## 5. Minimal Dependencies

- prefer built-in Linux tools  
- optional tools must degrade gracefully  
- installation must remain simple  

---

## 6. Graceful Degradation

If a dependency is missing, Argus must:

- NOT fail  
- return structured explanation  
- suggest required package  
- explain impact  

---

# Argus Tool Architecture Pattern (CRITICAL)

Every Argus tool MUST follow this pattern:

1. Argus tool is invoked via execution engine  
2. Argus tool calls one or more system tools  
3. System tools return structured `data`  
4. Argus tool aggregates signals  
5. Argus tool interprets system state  
6. Argus tool returns:

   - findings  
   - severity  
   - recommended actions  

---

# Tool Classification

Argus tools are divided into:

## Tier 1 — Core Tools (Required)

- must work on standard Ubuntu/Debian  
- no extra packages required  
- form the foundation of Argus  

---

## Tier 2 — Optional Tools (Enhanced)

- provide deeper insight  
- may require additional packages  
- must implement graceful fallback  

---

# Tier 1 — Core Tool Set

---

## System Overview

### Argus Tool: system_summary (IMPLEMENTED)

System Tools Used:

- system_info  

Capabilities:

- system health snapshot  
- CPU load analysis  
- memory usage evaluation  
- disk usage evaluation  
- OS identification  

Notes:

- first completed Argus tool  
- defines the reference implementation pattern  

---

### Argus Tool: process_top (NEXT)

System Tools Used:

- process_top (system tool)

Capabilities:

- identify high CPU processes  
- identify high memory processes  
- correlate with system load  

---

### Argus Tool: disk_layout

System Tools Used:

- disk_layout  

Capabilities:

- disk structure  
- mount relationships  

---

## Service Intelligence

### Argus Tool: service_status

System Tools Used:

- service_manager / systemctl wrapper  

Capabilities:

- active / inactive / failed  
- basic health interpretation  

---

### Argus Tool: service_list

System Tools Used:

- system tools wrapping systemctl list  

Capabilities:

- discover active services  
- detect failed services  

---

## Log Intelligence

### Argus Tool: log_recent_errors

System Tools Used:

- system_logs  

Capabilities:

- recent system errors  
- high-signal issue detection  

---

### Argus Tool: log_service

System Tools Used:

- system_logs  

Capabilities:

- service-specific troubleshooting  

---

### Argus Tool: kernel_log_check

System Tools Used:

- system_logs  

Capabilities:

- kernel-level issues  
- hardware/system faults  

---

## Disk & Resource Health

### Argus Tool: disk_usage

System Tools Used:

- disk_usage  

Capabilities:

- disk capacity monitoring  

---

### Argus Tool: disk_usage_breakdown

System Tools Used:

- disk_usage  

Capabilities:

- identify disk consumers  

---

### Argus Tool: memory_usage

System Tools Used:

- memory_usage  

Capabilities:

- memory usage analysis  

---

## Network Intelligence

### Argus Tool: network_interfaces

System Tools Used:

- network_interfaces  

---

### Argus Tool: routing_check

System Tools Used:

- network_interfaces  

---

### Argus Tool: listening_ports

System Tools Used:

- network_connections  

---

### Argus Tool: network_connectivity

System Tools Used:

- network_connections  

---

### Argus Tool: dns_check

System Tools Used:

- network_connections  

---

## Security Awareness

### Argus Tool: auth_log_scan

System Tools Used:

- system_logs  

---

### Argus Tool: sudo_activity_check

System Tools Used:

- system_logs  

---

## File & Config Discovery

### Argus Tool: find_file

System Tools Used:

- system-level search tools  

---

### Argus Tool: find_by_content

System Tools Used:

- system-level search tools  

---

### Argus Tool: read_file_safe

System Tools Used:

- system-level file read  

Constraints:

- file size limits required  

---

### Argus Tool: whereis_binary

System Tools Used:

- system-level lookup tools  

---

# Tier 2 — Optional Enhanced Tools

Same structure applies:

- Argus tool → system tool → dependency  

Examples:

- io_stats → system tool wrapper → iostat  
- dns_deep_check → system tool wrapper → dig  
- disk_health_smart → system tool wrapper → smartctl  

---

# Intelligence Layer (Behavior Model)

Argus intelligence is defined by interpretation, not just tool output.

---

## Production Personality (V1)

Argus must:

- explain the issue  
- describe where data was collected  
- present findings clearly  
- explain why it matters  
- recommend next steps  

---

## Output Model

Argus outputs include:

- findings (prioritized)  
- severity classification  
- recommended actions  

---

# Explicit Exclusions (V1)

Argus V1 does NOT include:

- automation or execution  
- service modification  
- configuration changes  
- training system features  
- long-term memory  
- multi-user support  
- cloud integration  

---

# Definition of Success

Argus V1 is successful if:

- system issues are clearly identified  
- troubleshooting time decreases  
- output is trusted and clear  
- installation is simple  
- system remains safe and predictable  

---

# Final Principle

Argus should feel simple, but be powered by structured, controlled system intelligence.

Argus is not a command layer.

Argus is an interpretation layer built on top of a controlled execution system.

---
````
