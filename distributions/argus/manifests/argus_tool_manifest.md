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
- preserve raw evidence for verification  

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
- preserve raw evidence from system tool data  

---

# Argus Tool Pattern (MANDATORY)

Every Argus tool must:

1. be invoked via execution engine  
2. call one or more system tools  
3. extract structured data  
4. evaluate system signals  
5. assign severity (if applicable)  
6. preserve raw evidence  
7. return:
   - findings  
   - severity  
   - recommended actions  
   - raw evidence  

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
- raw evidence preservation across system summary sources  

Notes:

- first completed Argus tool  
- aligned with the final raw-evidence diagnostic contract during Phase 5J closeout  

---

## process_top_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- process_top  

Capabilities:

- identify high CPU processes  
- identify high memory processes  
- preserve CPU and memory raw process evidence  

---

## memory_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- memory_usage  

Capabilities:

- evaluate memory usage  
- detect memory pressure  
- preserve raw memory command evidence  

---

## disk_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- disk_usage  

Capabilities:

- detect high disk usage  
- evaluate filesystem capacity  
- preserve raw disk usage evidence  

---

## network_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- network_interfaces  

Capabilities:

- evaluate interface state  
- detect inactive or abnormal interfaces  
- preserve raw network interface evidence  

---

## connections_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- network_connections  

Capabilities:

- evaluate connection volume  
- detect abnormal connection counts  
- preserve raw network connection evidence  

Notes:

- aligned with the final raw-evidence diagnostic contract during Phase 5J closeout  

---

## uptime_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- uptime_load  

Capabilities:

- evaluate system load  
- detect high load conditions  
- preserve raw uptime/load evidence  

Notes:

- aligned with the final raw-evidence diagnostic contract during Phase 5J closeout  

---

## logs_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- system_logs  

Capabilities:

- detect errors and warnings in logs  
- preserve raw log evidence when available  

Notes:

- aligned with the final raw-evidence diagnostic contract during Phase 5J closeout  
- raw log output may be empty when the underlying system log command returns no visible output  

---

## system_analysis (IMPLEMENTED)

Argus Tool

System Tools Used:

- disk_analysis
- memory_analysis
- network_analysis
- process_top_analysis

Capabilities:

- aggregate multiple Argus diagnostic signals  
- combine findings across core domains  
- determine highest system severity  
- preserve raw evidence from aggregated diagnostic tools  

Notes:

- first multi-signal Argus aggregation tool  
- established the system-level diagnostic view  

---

## process_top (LEGACY / REPLACED)

Argus Tool

System Tools Used:

- process_top  

Notes:

- replaced by process_top_analysis  

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
- follow the established Argus diagnostic pattern exactly  
- do NOT introduce new execution paths  
- do NOT call CommandRunner from Argus  
- do NOT duplicate system tool logic  
- reuse system tools  
- preserve raw evidence from system tool data  

---

# Final Rule

Argus must:

- provide structured interpretation  
- preserve raw evidence for verification  
- never expose raw command output without interpretation  
- remain read-only  
- operate within controlled execution  

Argus is an interpretation layer, not an execution layer.