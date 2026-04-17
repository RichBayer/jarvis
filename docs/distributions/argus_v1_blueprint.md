# Argus V1 – Tooling & Capability Blueprint

---

# Purpose

This document defines:

* the complete Argus V1 tool set
* capability scope and constraints
* command-level implementation mapping
* dependency handling model

This document ensures:

Argus V1 delivers high value while remaining simple, reliable, and easy to install.

---

# System Definition (V1)

Argus V1 is:

A read-only system intelligence layer that analyzes Linux systems, identifies issues, and explains them in plain English.

Argus V1 MUST:

* use real system data
* provide actionable insight
* remain safe (no modification of system state)
* require minimal installation complexity

---

# Core Design Rules

## 1. Read-Only Enforcement

Argus must NEVER:

* modify files
* restart services
* change system configuration
* execute destructive actions

---

## 2. Local Execution Only

* no external APIs required
* no telemetry
* no cloud dependencies

---

## 3. Minimal Dependencies

* prefer built-in Linux tools
* optional tools must degrade gracefully
* installation must remain simple

---

## 4. Graceful Degradation

If a required binary is missing, Argus must:

* NOT fail
* return a structured explanation
* suggest the required package
* explain impact of missing capability

---

# Tool Classification

Argus tools are divided into:

## Tier 1 — Core Tools (Required)

* must work on standard Ubuntu/Debian
* no extra packages required
* form the foundation of Argus

---

## Tier 2 — Optional Tools (Enhanced)

* provide deeper insight
* may require additional packages
* must implement graceful fallback

---

# Tier 1 — Core Tool Set

---

## System Overview

### Tool: system_summary

Commands:

* uptime
* free -h
* df -h
* cat /etc/os-release

Capabilities:

* system health snapshot
* CPU load (via uptime)
* memory usage
* disk usage
* OS identification

---

### Tool: process_top

Commands:

* ps aux --sort=-%cpu | head
* ps aux --sort=-%mem | head

Capabilities:

* identify high CPU processes
* identify high memory processes

---

### Tool: disk_layout

Commands:

* lsblk

Capabilities:

* disk structure
* mount relationships

---

## Service Intelligence

### Tool: service_status

Command:

* systemctl status <service>

Capabilities:

* active/inactive/failed
* basic health information

---

### Tool: service_list

Commands:

* systemctl list-units --type=service --state=running
* systemctl list-units --type=service --state=failed

Capabilities:

* discover active services
* detect failed services

---

## Log Intelligence

### Tool: log_recent_errors

Command:

* journalctl -p err -n 50

Capabilities:

* recent system errors
* high-signal issue detection

---

### Tool: log_service

Command:

* journalctl -u <service> -n 100

Capabilities:

* service-specific troubleshooting

---

### Tool: kernel_log_check

Command:

* dmesg | tail

Capabilities:

* kernel-level issues
* hardware/system faults

---

## Disk & Resource Health

### Tool: disk_usage

Command:

* df -h

Capabilities:

* disk capacity monitoring

---

### Tool: disk_usage_breakdown

Command:

* du -sh /var/* 2>/dev/null | sort -hr | head

Capabilities:

* identify disk consumers

---

### Tool: memory_usage

Command:

* free -h

Capabilities:

* memory usage snapshot

---

## Network Intelligence

### Tool: network_interfaces

Command:

* ip a

Capabilities:

* interface state
* IP addresses

---

### Tool: routing_check

Command:

* ip route

Capabilities:

* routing configuration
* gateway detection

---

### Tool: listening_ports

Command:

* ss -tuln

Capabilities:

* open ports
* listening services

---

### Tool: network_connectivity

Command:

* ping -c 3 8.8.8.8

Capabilities:

* internet connectivity

---

### Tool: dns_check

Command:

* nslookup google.com

Capabilities:

* DNS resolution validation

---

## Security Awareness

### Tool: auth_log_scan

Command:

* journalctl -u ssh | grep "Failed password"

Capabilities:

* detect failed login attempts

---

### Tool: sudo_activity_check

Command:

* journalctl | grep sudo

Capabilities:

* privilege escalation activity

---

## File & Config Discovery

### Tool: find_file

Command:

* find <path> -name "*pattern*"

Capabilities:

* locate files by name

---

### Tool: find_by_content

Command:

* grep -R "pattern" <path>

Capabilities:

* locate files by contents

---

### Tool: read_file_safe

Command:

* cat <file>

Constraints:

* file size limits required (future enforcement)

Capabilities:

* inspect configs/logs

---

### Tool: whereis_binary

Command:

* whereis <binary>

Capabilities:

* locate executables and configs

---

# Tier 2 — Optional Enhanced Tools

These tools improve depth but require dependency checks.

---

### Tool: io_stats

Command:

* iostat -x

Dependency:

* sysstat

Capabilities:

* disk I/O performance

---

### Tool: memory_pressure_detail

Command:

* vmstat

Capabilities:

* deeper memory insight

---

### Tool: fast_file_lookup

Command:

* locate <file>

Dependency:

* mlocate / plocate

Capabilities:

* faster file discovery

---

### Tool: dns_deep_check

Command:

* dig google.com

Dependency:

* dnsutils

Capabilities:

* deeper DNS analysis

---

### Tool: open_files_for_process

Command:

* lsof

Capabilities:

* file usage by process

---

### Tool: disk_health_smart

Command:

* smartctl -H /dev/sdX

Dependency:

* smartmontools

Capabilities:

* hardware disk health

---

# Intelligence Layer (Behavior Model)

Argus intelligence is not just tools.

It is how those tools are interpreted and presented.

---

## Production Personality (V1)

This is the ONLY personality included in Argus V1 standalone.

---

### Behavior

Argus must:

* explain what the issue is
* state where it looked (logs, services, system state)
* describe what it found
* explain why the finding matters
* recommend next steps

---

### Output Style

Production Argus should provide both:

* conceptual explanation
* practical next steps

This includes:

* describing the problem clearly
* referencing relevant system data
* recommending how to verify or resolve the issue
* providing commands when appropriate

---

### Interaction Model

* user can ask follow-up questions
* Argus provides clarification
* Argus improves understanding when prompted
* Argus does NOT default to teaching mode

---

## Training Personality (Not Part of V1)

This personality is only available in the training environment.

---

### Behavior

Argus should:

* describe symptoms
* suggest where to investigate
* guide the user logically
* allow independent troubleshooting first

---

### Guidance Progression

1. Initial guidance → where to look  
2. Follow-up → more specific hints  
3. Coaching → full walkthrough if user is stuck  

---

### Coaching Mode

When triggered, Argus provides:

* step-by-step troubleshooting
* reasoning behind each step
* explanation of root cause
* mentoring-style guidance

---

# Intelligence Capabilities

These apply across personalities.

---

## Issue Prioritization

* rank issues by severity
* highlight high-impact problems

---

## Plain-English Explanation

* translate logs and output
* remove technical noise

---

## Recommended Actions

* suggest next steps
* never execute changes

---

## Executive Summary Mode

Example:

argus --summary

Output:

* simplified system health
* non-technical explanation

---

## Explain System Mode

Example:

argus explain

Output:

* inferred system role
* high-level system purpose

---

# Explicit Exclusions (V1)

Argus V1 does NOT include:

* automation or execution
* service modification
* configuration changes
* training system features
* session tracking
* performance scoring
* adaptive behavior
* cloud integration
* monitoring integrations
* long-term memory
* multi-user support
* perception / home automation features

---

# Definition of Success

Argus V1 is successful if:

* users quickly understand system issues
* troubleshooting time decreases
* output is trusted and clear
* installation is simple
* system remains safe and predictable

---

# Final Principle

Argus should feel simple, but be powered by structured, controlled system intelligence.

V1 must remain focused, predictable, and immediately useful.

---

# End of Document