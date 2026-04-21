# NeuroCore Documentation Index

---

## 📖 Overview

This directory contains the complete documentation for the NeuroCore system.

The documentation is organized to reflect how the system is actually built and used:

- Vision (what and why)
- Architecture (how it works)
- Execution & Core Systems (how it behaves)
- Distributions (user-facing systems)
- Infrastructure (environment and layout)
- Development & Operations
- Build History (full evolution of the system)

---

## 🧠 Vision (Start Here)

If you're new, start here to understand the system at a high level.

- 👉 [NeuroCore Vision](./architecture/neurocore_vision.md)
- 👉 [Argus ACLI Vision](./vision/argus_acli_vision.md)
- 👉 [Argus Lab Vision](./vision/argus_lab_vision.md)

---

## 🏗 Core Architecture

Defines how NeuroCore is structured and how all components interact.

- 👉 [System Architecture](./architecture/system_architecture.md)
- 👉 [Platform Ecosystem](./architecture/platform_ecosystem.md)
- 👉 [System State](./architecture/system_state.md)

---

## ⚙️ Execution & Core Systems

Detailed breakdown of how the system operates internally.

- 👉 [Control Plane](./architecture/control_plane.md)
- 👉 [Tool Execution System](./architecture/tool_execution.md)
- 👉 [Task Engine](./architecture/task_engine.md)
- 👉 [Observability](./architecture/observability.md)
- 👉 [Evaluation Framework](./architecture/evaluation_framework.md)
- 👉 [Security Policy](./architecture/security_policy.md)

---

## 🧩 Distributions (Argus)

User-facing systems built on top of NeuroCore.

- 👉 [Argus V1 Blueprint](./distributions/argus_v1_blueprint.md)
- 👉 [Argus ACLI Specification](./distributions/argus/acli_spec.md)

---

## 🏠 Infrastructure & Environment

System layout, infrastructure design, and environment mapping.

- 👉 [Repository Map](./infrastructure/neurocore_repository_map.txt)
- 👉 [System Map](./infrastructure/neurocore_system_map.txt)
- 👉 [Home System Map](./infrastructure/home_system_map.md)
- 👉 [Home Infrastructure](./infrastructure/home_infrastructure.md)

---

## 🤖 AI Operations

How the AI system is operated, resumed, and interacted with.

- 👉 [Resume Prompt (Primary)](./ai-operations/resume_prompt_compressed.md)
- 👉 [Context Loading Strategy](./ai-operations/context_loading_strategy.md)

---

## 🧪 Design Documents

In-progress and phase-specific design work.

- 👉 [Phase 5I – Real Execution](./design/phase_5i_real_execution.md)

---

## 🖥 Hardware & Physical System

Physical infrastructure and hardware planning.

- 👉 [Home AI Hardware](./hardware/home_ai_hardware.md)

---

## 🧪 Build Logs (Full Development History)

Complete system evolution from initial build to current state.

👉 [Build Logs Directory](../build-logs/)

---

### 📂 All Build Logs

- 👉 [000 – Foundation](../build-logs/000_foundation.md)
- 👉 [001 – Runtime Stack](../build-logs/001_runtime_stack.md)
- 👉 [002 – Interface Layer](../build-logs/002_interface_layer.md)
- 👉 [003 – Knowledge Layer](../build-logs/003_knowledge_layer.md)
- 👉 [004 – Knowledge Retrieval](../build-logs/004_knowledge_retrieval.md)
- 👉 [005 – Logic Layer Router](../build-logs/005_logic_layer_router.md)
- 👉 [006 – RAG Reasoning Integration](../build-logs/006_rag_reasoning_integration.md)
- 👉 [007 – Backup and Rebuild Foundations](../build-logs/007_backup_and_rebuild_foundations.md)
- 👉 [008 – Runtime Performance and API Migration](../build-logs/008_runtime_performance_and_api_migration.md)
- 👉 [009 – Daemon Foundation](../build-logs/009_neurocore_daemon_foundation.md)
- 👉 [010 – Runtime Integration](../build-logs/010_runtime_integration.md)
- 👉 [011 – CLI Interface Layer](../build-logs/011_cli_interface_layer.md)
- 👉 [012 – Streaming Pipeline and CLI Behavior](../build-logs/012_streaming_pipeline_and_cli_behavior.md)
- 👉 [013 – RAG Metadata and Grounding](../build-logs/013_rag_metadata_and_grounding.md)
- 👉 [014 – Session Memory and Query Rewriting](../build-logs/014_session_memory_query_rewriting_and_knowledge_correction.md)
- 👉 [015 – CLI Piped Input Ingestion](../build-logs/015_cli_piped_input_ingestion.md)
- 👉 [016 – Runtime Control Plane Enforcement](../build-logs/016_runtime_control_plane_enforcement.md)
- 👉 [017 – Execution Layer and Control Integration](../build-logs/017_execution_layer_and_control_integration.md)
- 👉 [018 – Observability and Tracing](../build-logs/018_observability_and_tracing.md)
- 👉 [019 – Real Tool Execution and System Info](../build-logs/019_real_tool_execution_and_system_info.md)

---

### ⭐ Suggested Starting Points

If you don’t want to read everything:

- 👉 000 – Foundation  
- 👉 009 – Daemon Foundation  
- 👉 012 – Streaming Pipeline  
- 👉 016 – Control Plane Enforcement  
- 👉 017 – Execution Layer Integration  
- 👉 019 – Real Tool Execution  

These represent major system milestones.
---

## 🧭 How to Navigate

### If you're new:
- Start with **NeuroCore Vision**
- Then read **Argus ACLI Vision**
- Then **Argus Lab Vision**
- Then check **System State**

---

### If you're technical:
- Start with **System Architecture**
- Then **Control Plane**
- Then **Tool Execution System**
- Then explore **Build Logs**

---

### If you're interested in using the system:
- Read **Argus ACLI Vision**
- Then **Argus Blueprint**
- Then explore architecture as needed

---

## 💡 Final Note

This repository reflects a real system under active development.

Documentation is:

- structured  
- layered  
- aligned with actual system behavior  

This is not theoretical.

This is a working platform being built in real time.

---

# End of Document