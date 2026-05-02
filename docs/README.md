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
- 👉 [Argus Output & Tool Contract](./architecture/argus_output_and_tool_contract.md)
- 👉 [Phase-Aware Development](./architecture/phase_aware_development.md)

---

## ⚙️ Execution & Core Systems

Detailed breakdown of how the system operates internally.

- 👉 [Control Plane](./architecture/control_plane.md)
- 👉 [Tool Execution System](./architecture/tool_execution.md)
- 👉 [Tool Pattern](./architecture/tool_pattern.md)
- 👉 [Task Engine](./architecture/task_engine.md)
- 👉 [Observability](./architecture/observability.md)
- 👉 [Evaluation Framework](./architecture/evaluation_framework.md)
- 👉 [Security Policy](./architecture/security_policy.md)

---

## 🧩 Distributions (Argus)

User-facing systems built on top of NeuroCore.

- 👉 [Argus V1 Blueprint](./distributions/argus_v1_blueprint.md)
- 👉 [Argus ACLI Specification](./distributions/argus/acli_spec.md)
- 👉 [Argus Distribution & Deployment Plan](./distributions/argus/argus_distribution_and_deployment.md)
- 👉 [Argus Tool Manifest](../distributions/argus/manifests/argus_tool_manifest.md)

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
- 👉 [Documentation Closeout Protocol](./ai-operations/documentation_closeout_protocol.md)
- 👉 [Mid-Phase Reset Protocol](./ai-operations/mid_phase_reset_protocol.md)

---

## 🧪 Design Documents

In-progress and phase-specific design work.

- 👉 [Phase 5I – Real Execution](./design/phase_5i_real_execution.md)
- 👉 [Argus Tool Layer](./design/argus_tool_layer.md)
- 👉 [Argus System Summary V1](./design/argus_system_summary_v1.md)
- 👉 [Phase 5J – Argus Core Tool Expansion](./design/phase_5j_argus_core_tool_expansion.md)
- 👉 [Argus ACLI User Experience Layer](./design/argus_acli_user_experience_layer.md)

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
- 👉 [020 – NeuroCore System Tool Expansion](../build-logs/020_neurocore_system_tool_expansion.md)
- 👉 [021 – Argus Tool Layer Initial](../build-logs/021_argus_tool_layer_initial.md)
- 👉 [022 – Structured Tool Contract](../build-logs/022_structured_tool_contract.md)
- 👉 [023 – System Tool Structuring and Normalization](../build-logs/023_system_tool_structuring_and_normalization.md)
- 👉 [024 – Argus Tool Layer Foundation and Expansion](../build-logs/024_argus_tool_layer_foundation_and_expansion.md)
- 👉 [025 – System Analysis Multi-Signal Aggregation and CLI UX](../build-logs/025_system_analysis_multi_signal.md)

---

### ⭐ Suggested Starting Points

If you don’t want to read everything:

- 👉 [000 – Foundation](../build-logs/000_foundation.md)
- 👉 [009 – Daemon Foundation](../build-logs/009_neurocore_daemon_foundation.md)
- 👉 [012 – Streaming Pipeline](../build-logs/012_streaming_pipeline_and_cli_behavior.md)
- 👉 [016 – Control Plane Enforcement](../build-logs/016_runtime_control_plane_enforcement.md)
- 👉 [017 – Execution Layer Integration](../build-logs/017_execution_layer_and_control_integration.md)
- 👉 [019 – Real Tool Execution](../build-logs/019_real_tool_execution_and_system_info.md)
- 👉 [023 – System Tool Structuring and Normalization](../build-logs/023_system_tool_structuring_and_normalization.md)
- 👉 [024 – Argus Tool Layer Foundation and Expansion](../build-logs/024_argus_tool_layer_foundation_and_expansion.md)
- 👉 [025 – System Analysis Multi-Signal Aggregation and CLI UX](../build-logs/025_system_analysis_multi_signal.md)

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
- Then **Tool Pattern**
- Then explore **Build Logs**

---

### If you're interested in using the system:
- Read **Argus ACLI Vision**
- Then **Argus Blueprint**
- Then **Argus ACLI Specification**
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