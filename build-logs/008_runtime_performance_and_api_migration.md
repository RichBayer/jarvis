# Build Log 008 — Runtime Performance Optimization & API Migration

## Overview

This milestone focused on resolving severe response latency issues in the NeuroCore system and transitioning from a CLI-based execution model to a proper API-based architecture.

Initial response times were approximately **2–3 minutes per query**, making the system impractical for real-world use.

After optimization, response times were reduced to approximately **4–10 seconds**, enabling real-time interaction.

---

## Problems Identified

### 1. Subprocess-Based Model Execution

The logic router originally used:

```python
subprocess.run(["ollama", "run", "llama3.1:8b"])
```

This caused:

- repeated process spawning
- model reinitialization behavior
- blocking execution
- high latency

---

### 2. Embedding Model Reloading

The HuggingFace embedding model was being initialized during each query.

Symptoms:

- repeated "Loading weights" messages
- unnecessary overhead

---

### 3. Chroma Retrieval Reinitialization

The knowledge retrieval system recreated:

- Chroma client
- vector store
- index
- retriever

on every query.

This caused significant delays before the model was even invoked.

---

### 4. Blocking API Behavior

Even after switching to the Ollama API, responses were delayed due to:

- non-streaming requests
- full-response buffering

---

### 5. Misleading Bottleneck Assumption

Initial assumption:

- model inference was slow

Actual finding:

- model inference was fast (~4 seconds)
- latency was caused by upstream architecture

---

## Solutions Implemented

### 1. API-Based Model Invocation

Replaced subprocess execution with HTTP API:

```python
requests.post("http://localhost:11434/api/generate", ...)
```

Result:

- eliminated process overhead
- enabled persistent model usage

---

### 2. Streaming Response Handling

Implemented streaming output:

- real-time token display
- improved perceived responsiveness

---

### 3. Global Initialization of Retrieval Components

Moved initialization outside function scope:

```python
chroma_client = ...
index = ...
retriever = ...
```

Result:

- eliminated repeated setup cost per query

---

### 4. Embedding Model Initialization Optimization

Loaded embedding model once at module level:

```python
Settings.embed_model = HuggingFaceEmbedding(...)
```

---

### 5. Output Length Control

Added:

```python
"num_predict": 200
```

Result:

- reduced generation time
- prevented overly long responses

---

## Performance Results

| Stage | Before | After |
|------|--------|------|
| Retrieval + Setup | ~2 minutes | <1 second |
| Model Response | ~60–120 sec | ~4–10 sec |
| Total | ~2–3 minutes | ~4–10 seconds |

---

## Key Lessons

- Most latency in AI systems comes from architecture, not models
- Avoid subprocess-based execution for LLM integration
- Persistent components are critical for performance
- Streaming dramatically improves usability
- Always validate assumptions with direct timing tests

---

## System State After This Milestone

NeuroCore now supports:

- fast API-based LLM interaction
- efficient retrieval pipeline
- real-time streaming responses
- significantly improved usability

The system is now ready for:

- persistent runtime implementation
- tool execution integration
- interactive CLI workflows

---

## Next Step

Build NeuroCore persistent runtime:

- interactive CLI interface
- command piping support
- always-available assistant behavior