# Home Infrastructure Map

Owner: Richard Bayer

Purpose:
Document the structure of the home computing environment used for the Jarvis AI system, Linux practice environments, and virtualization lab infrastructure.

This file provides a **quick architectural overview** of machines, roles, networking, and storage.

Build logs and detailed setup steps are documented separately in the respective project repositories.

---

# Network Architecture

Primary connectivity is provided through **Tailscale**, creating a secure private mesh network between all machines.

Devices can communicate using either:

* local LAN IP addresses
* Tailscale mesh IP addresses
* MagicDNS hostnames

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
AMD Ryzen 7 5800X (16 threads)

RAM
32 GB

GPU
NVIDIA RTX 3060 (12 GB VRAM)

Motherboard
Lenovo 3716 (B550 chipset)

---

# Storage Layout

C:
Windows operating system

G:
Primary NVMe storage
Used for AI workspace and WSL filesystem

/mnt/g/ai contains:

models
runtime
memory
projects
logs
backups

V:
VMware virtual machine storage

4 TB External USB HDD

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

# Future Expansion

Possible future additions include:

additional Proxmox nodes
automation via Ansible
log analysis integration with Jarvis
home automation integration
AI-assisted infrastructure monitoring

