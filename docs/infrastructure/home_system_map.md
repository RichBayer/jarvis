# Home System Map

This document provides visual diagrams of the physical hardware, system architecture,
and future expansion plans for the home computing infrastructure.

Diagrams are maintained in plain text so they remain version-controlled,
readable on GitHub, and easy to update.

---

# System Architecture

```text
                    Internet
                        │
                    Tailscale
                        │
            ┌────────────────────────┐
            │     Lenovo Legion      │
            │  Ryzen 7 5800 CPU      │
            │  32GB RAM              │
            │  RTX 3060 GPU          │
            └────────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                                 │
    Windows 11                        Storage
        │                                 │
 ┌──────┴──────────┐            ┌──────────┴───────────┐
 │                 │            │                      │
WSL Ubuntu     VMware WS     C: Windows             G: NeuroCore
 │                 │          256GB NVMe             2TB NVMe
 │            ┌────┴─────┐
 │            │          │
NeuroCore AI Proxmox   LinuxPractice
Platform      VM           VM
```

---

# Lenovo Legion Hardware Layout

```text
           ┌─────────────────────────┐
           │           CPU           │
           │      Ryzen 7 5800       │
           └────────────┬────────────┘
                        │
                M.2 Slot #1
              256GB NVMe (C:)
                        │
           ┌────────────┴────────────┐
           │                         │
      M.2 Slot #2               M.2 Key-E
   Samsung 990 Pro 2TB          WiFi Card
        (G: Drive)
           │
       PCIe x16 Slot
         RTX 3060
           │
       PCIe x1 Slot
     (Expansion Available)
```

---

# Future Infrastructure Architecture

```text
                 ┌─────────────────┐
                 │  Lenovo Legion  │
                 │  AI Compute     │
                 │  GPU Inference  │
                 └────────┬────────┘
                          │
            ┌─────────────┼─────────────┐
            │                           │
     Infrastructure Node           Storage Node
        (Mini Server)                 (NAS)
     Automation + APIs         Models + Archives
```
