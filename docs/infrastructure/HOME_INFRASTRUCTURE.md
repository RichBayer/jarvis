# Home Infrastructure Overview

Owner: Richard Bayer

Purpose:
Document the structure of the home computing environment used for the Jarvis AI system, Linux practice environments, and virtualization lab infrastructure.

This file provides a quick architectural overview of machines, roles, networking, storage, and hardware expansion capability.

Build logs and detailed setup steps are documented separately in the respective project repositories.

For visual diagrams of the system architecture and hardware layout,
see:

**[HOME_SYSTEM_MAP.md](HOME_SYSTEM_MAP.md)**

---

# Network Architecture

Primary connectivity is provided through Tailscale, creating a secure private mesh network between all machines.

Devices can communicate using either:

local LAN IP addresses  
Tailscale mesh IP addresses  
MagicDNS hostnames  

Example SSH access:

ssh richb@lenovolegion  
ssh richb@linuxpractice  

---

# Primary Compute Node

Hostname  
LenovoLegion  

Role  
Primary workstation and infrastructure host  

Operating System  
Windows 11 Home  

Hardware

CPU  
AMD Ryzen 7 5800 (8 cores / 16 threads)

RAM  
32 GB (2 x 16GB DIMMs)

GPU  
NVIDIA RTX 3060 (12 GB VRAM)

Motherboard  
Lenovo 3716 (B550 chipset)

Platform notes

AMD B550 platform  
PCIe 4.0 support from CPU lanes  
Chipset provides additional PCIe expansion lanes  

---

# Motherboard Expansion Layout

The Lenovo 3716 motherboard provides the following expansion interfaces.

M.2 NVMe Slot #1  
Location: under CPU cooler area  
Device installed: Samsung 256GB NVMe  
Role: Windows boot drive  

M.2 NVMe Slot #2  
Location: above GPU area  
Device installed: Samsung 990 Pro 2TB  
Role: primary high-speed storage  

M.2 Key-E Slot  
Location: near rear IO area  
Device installed: WiFi / Bluetooth card  

PCIe x16 Slot  
Device installed: NVIDIA RTX 3060 GPU  

PCIe x1 Slot  
Currently unused  
Available for expansion  

Expansion capability notes

The PCIe x1 slot can support:

NVMe adapter card  
10Gb networking card  
capture card  
additional storage controllers  

An NVMe adapter in this slot would operate at approximately 1GB/s bandwidth (PCIe 3.0 x1).

---

# Storage Layout

C:
256GB Samsung NVMe

Windows operating system  
system tools  
applications  

G:
2TB Samsung 990 Pro NVMe

Primary high speed workspace

Used for:

Jarvis AI environment  
personal files  
games  
development repositories  

Jarvis filesystem structure

/mnt/g/ai contains:

models  
runtime  
memory  
projects  
logs  
backups  

V:
1TB Western Digital HDD

Used for:

VMware virtual machines  
homelab experimentation  

External Storage

4TB Seagate Expansion USB HDD

Used for:

backups  
ISO images  
future archive storage  

---

# AI Platform (Jarvis)

Environment  
WSL2 Ubuntu

Repository location

~/ai/projects/jarvis

Major components

Ollama  
local LLM runtime  

Open WebUI  
browser interface (Docker container)  

Chroma  
vector database  

LlamaIndex  
document ingestion and retrieval  

Python runtime

~/ai/runtime/python/jarvis-env

GPU acceleration provided through CUDA passthrough from the RTX 3060.

Web interface

http://localhost:3000

Ollama API

localhost:11434

---

# Virtualization Layer

Hypervisor

VMware Workstation Pro

Host machine

LenovoLegion (Windows 11)

VMware virtual networks

VMnet8  
NAT network  

VMnet1  
Host-only network  

---

# Virtual Machines

## Proxmox Homelab

Environment

Nested Proxmox VE 8.3

Hosted inside VMware Workstation

Purpose

Infrastructure lab for:

Linux server practice  
VM deployment  
container experimentation  
future automation and orchestration work  

Networking

Static IP

192.168.1.149

Web interface

https://192.168.1.149:8006

Remote access

Tailscale node

100.94.167.49

SSH access

ssh richb@homelab

---

## LinuxPractice VM

Operating System

Rocky Linux 9.7 (Blue Onyx)

Purpose

Dedicated Linux training environment for:

Bash scripting  
Linux command practice  
system administration exercises  

Networking

LAN address

192.168.86.226

Tailscale address

100.70.61.34

Access

ssh richb@linuxpractice

---

# Remote Access Devices

## Lenovo Yoga Laptop

Primary development console

Used for

SSH access  
VS Code remote editing  
Jarvis development  

Connected via Tailscale

---

## Galaxy S24 Phone

Mobile infrastructure access

Tool

Termius SSH client

Used for quick remote administration tasks

---

# System Architecture Overview

Lenovo Legion (Physical Host)

Windows 11
│
├─ WSL Ubuntu
│   └─ Jarvis AI Platform
│
└─ VMware Workstation
    ├─ Proxmox Homelab VM
    └─ LinuxPractice Rocky VM

All machines connected through Tailscale mesh networking.

---

# Design Goals

Local-first AI infrastructure  
Secure remote administration  
Hands-on Linux system administration practice  
Automation experimentation  
Professional portfolio development  

---

# Hardware Expansion Strategy

The Legion workstation currently acts as:

AI compute node  
development workstation  
virtualization host  

As Jarvis evolves, hardware upgrades will focus on maintaining balanced system performance rather than maximizing a single component.

Priority order is based on likely bottlenecks.

---

# Upgrade Roadmap

Stage 1 — Storage Architecture Improvement

Replace current 256GB Windows NVMe with a 2TB NVMe drive.

New layout:

2TB NVMe (C:)  
Windows  
applications  
personal files  
games  

2TB Samsung 990 Pro (G:)  
Jarvis AI workspace  

Jarvis components on dedicated drive:

vector database  
embeddings  
datasets  
AI models  

Benefits

reduces disk contention  
isolates AI workloads  
provides additional system storage headroom  

---

Stage 2 — Memory Expansion

Upgrade RAM

32GB → 64GB

Configuration

4 x 16GB DDR4

Benefits

larger document ingestion runs  
bigger vector database caches  
multiple AI agents simultaneously  
reduced disk swapping  

---

Stage 3 — VM Storage Upgrade

Replace current 1TB mechanical HDD with SATA SSD.

Benefits

dramatically faster VM boot times  
better Proxmox nested performance  
improved homelab usability  

---

Stage 4 — NVMe Expansion

Install PCIe x1 NVMe adapter in available expansion slot.

Purpose

additional high-speed storage for:

AI datasets  
model experimentation  
future indexing workloads  

---

Stage 5 — Dedicated Infrastructure Node

Introduce a small secondary server.

Possible hardware

refurbished Lenovo ThinkCentre Tiny  
Dell OptiPlex Micro  
HP EliteDesk Mini  

Purpose

24/7 infrastructure services

Home Assistant  
automation tools  
monitoring stack  
API services  

Legion remains the primary AI compute node.

---

Stage 6 — Future AI Compute Expansion

Potential GPU upgrade when larger models become desirable.

Options may include GPUs with:

16GB VRAM  
24GB VRAM  

Benefits

larger model support  
higher context windows  
multiple model execution  

---

# Long-Term Architecture Vision

Jarvis infrastructure will gradually evolve toward a distributed architecture.

AI compute node  
Legion workstation  

Infrastructure node  
automation services  

Storage node  
NAS or backup server  

All systems connected through Tailscale mesh networking.

---

# Future Expansion Possibilities

additional Proxmox nodes  
automation via Ansible  
log analysis integration with Jarvis  
home automation integration  
AI-assisted infrastructure monitoring  
distributed AI services
