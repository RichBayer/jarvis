# Jarvis System Architecture

## Compute Node

Primary machine: Lenovo Legion Desktop

CPU: AMD Ryzen 7 5800X  
RAM: 32GB  
GPU: NVIDIA RTX 3060 12GB  
OS: Windows 11 with WSL2 Ubuntu

---

## Storage Layout

Primary NVMe (G:)

G:\ai
models
runtime
memory
projects
logs
backups

External HDD (4TB)

Archive storage  
camera recordings  
AI memory archive  
system backups

---

## AI Runtime Layer

Runs inside WSL Ubuntu.

Core components:

Ollama – model runtime  
Open WebUI – chat interface  
Whisper – speech-to-text  
Piper – text-to-speech  
Chroma – vector database  
LlamaIndex – document indexing

---

## Interface Layer

User interfaces include:

Tablets
Voice nodes
Web interface
Mobile devices via Tailscale

---

## Perception Layer

Sensors feeding the AI:

Microphones
Cameras
Motion sensors
Door sensors
Smart devices

---

## Automation Layer

Home Assistant provides integration with:

lights
cameras
sensors
automation rules

Communication handled through MQTT.

---

## Design Goal

Centralized intelligence with distributed interaction points.

One powerful AI brain, many lightweight terminals.
