````markdown
# Argus V1 – Tool Manifest

---

# Purpose

This document defines the executable Argus tool layer for V1.

It maps:

- Argus tools → system tools  
- system tools → system commands  
- tool tiers → core vs optional  
- dependencies → required binaries  
- behavior → execution + fallback rules  

This document is the **build checklist** for Argus tool expansion.

---

# Execution Model (CRITICAL)

Argus tools DO NOT execute commands.

All execution follows:

```
control_plane
→ execution_engine
→ argus_tool
→ system_tool(s)
→ command_runner
→ operating system
```

---

# Tool Layer Separation

## System Tools

- perform execution  
- call CommandRunner  
- return structured data  

## Argus Tools

- compose system tools  
- aggregate signals  
- interpret system state  
- return findings and recommendations  

---

# Structured Output Requirement

All system tools must return:

```
{
  "status": "...",
  "message": "...",
  "data": { ... }
}
```

Argus tools MUST:

- consume `data`  
- NOT parse formatted message output  
- NOT rely on string matching  

---

# Argus Tool Pattern (MANDATORY)

Every Argus tool must:

1. be invoked via execution engine  
2. call one or more system tools  
3. extract structured data  
4. evaluate system signals  
5. assign severity (if applicable)  
6. return:
   - findings  
   - severity  
   - recommended actions  

---

# Tool Classification

## Tier 1 — Core Tools

- must work on standard Ubuntu/Debian  
- no additional dependencies  
- required for Argus V1  

---

## Tier 2 — Optional Tools

- provide deeper insight  
- may require additional packages  
- must implement graceful fallback  

---

# Tier 1 — Core Tool Set

---

## system_summary (IMPLEMENTED)

Argus Tool

System Tools Used:

- system_info  

Capabilities:

- system health overview  
- CPU load interpretation  
- memory usage analysis  
- disk usage analysis  
- OS identification  

Notes:

- first completed Argus tool  
- defines the reference pattern  

---

## process_top (NEXT)

Argus Tool

System Tools Used:

- process_top  

Capabilities:

- identify high CPU processes  
- identify high memory processes  
- correlate with system load  

---

## disk_layout

Argus Tool

System Tools Used:

- disk_layout  

---

## service_status

Argus Tool

System Tools Used:

- service_manager / systemctl wrapper  

---

## service_list

Argus Tool

System Tools Used:

- system tools wrapping systemctl list  

---

## log_recent_errors

Argus Tool

System Tools Used:

- system_logs  

---

## log_service

Argus Tool

System Tools Used:

- system_logs  

---

## kernel_log_check

Argus Tool

System Tools Used:

- system_logs  

---

## disk_usage

Argus Tool

System Tools Used:

- disk_usage  

---

## disk_usage_breakdown

Argus Tool

System Tools Used:

- disk_usage  

---

## memory_usage

Argus Tool

System Tools Used:

- memory_usage  

---

## network_interfaces

Argus Tool

System Tools Used:

- network_interfaces  

---

## routing_check

Argus Tool

System Tools Used:

- network_interfaces  

---

## listening_ports

Argus Tool

System Tools Used:

- network_connections  

---

## network_connectivity

Argus Tool

System Tools Used:

- network_connections  

---

## dns_check

Argus Tool

System Tools Used:

- network_connections  

---

## auth_log_scan

Argus Tool

System Tools Used:

- system_logs  

---

## sudo_activity_check

Argus Tool

System Tools Used:

- system_logs  

---

## find_file

Argus Tool

System Tools Used:

- system-level search tools  

---

## find_by_content

Argus Tool

System Tools Used:

- system-level search tools  

---

## read_file_safe

Argus Tool

System Tools Used:

- system-level file read  

Constraints:

- file size limits required  

---

## whereis_binary

Argus Tool

System Tools Used:

- system-level lookup tools  

---

# Tier 2 — Optional Tools

Same structure applies:

Argus Tool → System Tool → Command → Dependency

---

## io_stats

System Tool → iostat  
Dependency → sysstat  

---

## memory_pressure_detail

System Tool → vmstat  

---

## fast_file_lookup

System Tool → locate  
Dependency → mlocate / plocate  

---

## dns_deep_check

System Tool → dig  
Dependency → dnsutils  

---

## open_files_for_process

System Tool → lsof  

---

## disk_health_smart

System Tool → smartctl  
Dependency → smartmontools  

---

# Failure Handling Standard

If a dependency is missing, return:

```
status: unavailable
reason: missing dependency
package: suggested install package
impact: capability limitation
```

---

# Build Rules (CRITICAL)

- implement ONE Argus tool at a time  
- follow system_summary pattern exactly  
- do NOT introduce new execution paths  
- do NOT call CommandRunner from Argus  
- do NOT duplicate system tool logic  
- reuse system tools  

---

# Final Rule

Argus must:

- provide structured interpretation  
- never expose raw command output  
- remain read-only  
- operate within controlled execution  

Argus is an interpretation layer, not an execution layer.
````
