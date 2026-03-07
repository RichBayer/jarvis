# Build Log 000 – Foundation

Date: March 2026

## Initial Environment Setup

WSL2 Ubuntu installed on Windows 11.

Original distribution exported from the C drive and re-imported onto the NVMe drive.

New WSL storage location:

G:\wsl\Ubuntu

---

## AI Workspace

AI workspace created on NVMe:

/mnt/g/ai

Directory structure:

models  
runtime  
memory  
projects  
logs  
backups

A symbolic link was created:

~/ai -> /mnt/g/ai

---

## Git Repository

GitHub repository created:

RichBayer/jarvis

Repository cloned to:

~/ai/projects/jarvis

SSH authentication configured between WSL and GitHub.

---

## Current Status

Project documentation structure created.

Next phase will begin installation of the AI runtime stack.
