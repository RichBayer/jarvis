# Build Log 011 – CLI Interface Layer

Date: April 2026

## Objective

Up to this point, NeuroCore could only be interacted with through manual socket testing.

The goal for this phase was to introduce a real interface layer so the system could be used from the command line in a natural way.

Target usage:

    python scripts/ai_cli.py "hello"

This phase connects the full system pipeline:

    CLI → daemon → runtime → router → knowledge → model → response

into a single usable flow.

---

## System State Before This Phase

Previous interaction flow:

    manual Python test script
    ↓
    daemon (UNIX socket)
    ↓
    runtime manager
    ↓
    router
    ↓
    response printed manually

The system was functional, but not usable.

---

## CLI Interface Introduced

A new CLI client was created:

    scripts/ai_cli.py

Responsibilities:

- connect to /tmp/neurocore.sock  
- send structured requests  
- receive responses  
- print clean output to terminal  

Request format:

    {
      "type": "query",
      "user": "richard",
      "mode": "cli",
      "data": {
        "input": "hello"
      }
    }

This format is designed to support future interfaces (web, voice, API) without changing the core system.

---

## First End-to-End Attempt

Initial test:

    python scripts/ai_cli.py "hello"

The request reached the daemon successfully, but failed in the runtime layer.

Error:

    No query text provided

---

## Issue 1 – Request Format Mismatch

The CLI and runtime were using different request structures.

Runtime expected:

    {
      "type": "query",
      "payload": {
        "text": "..."
      }
    }

CLI sent:

    {
      "data": {
        "input": "..."
      }
    }

### Fix

A normalization layer was added in the daemon to convert incoming requests into the runtime format.

This keeps the runtime clean and allows the daemon to act as the protocol boundary.

---

## Issue 2 – Partial Socket Reads

The daemon originally used:

    conn.recv(4096)

This only reads a single chunk and can result in incomplete data.

### Fix

Implemented a full read loop:

    def recv_full(conn):

This ensures the entire request is received before processing.

---

## Issue 3 – Broken Pipe Crash

During the first query, the knowledge system initializes:

- embedding model  
- Chroma vector store  

This takes time.

The CLI timed out and closed the connection early.

The daemon then attempted to send a response and crashed:

    BrokenPipeError: [Errno 32] Broken pipe

### Screenshot

![Daemon Broken Pipe Crash](../docs/screenshots/interface/neurocore-daemon-broken-pipe-crash.png)

### Fix

Wrapped all send operations to safely handle client disconnects.

The daemon now logs the disconnect instead of crashing and continues running.

---

## Issue 4 – Deadlock Between CLI and Daemon

After fixing the crash, the system stalled completely.

- daemon waited for client to finish sending data  
- CLI waited for daemon response  

Result:

    CLI timeout

### Screenshot

![CLI Timeout](../docs/screenshots/interface/neurocore-cli-timeout.png)

### Root Cause

The daemon was waiting for the client to close the connection before continuing.

The client never signaled that it was done sending.

### Fix

Added:

    client.shutdown(socket.SHUT_WR)

This signals the end of the request and allows the daemon to proceed immediately.

---

## Issue 5 – Response Completion Signaling

After fixing the deadlock, the CLI still waited longer than expected.

### Fix

The daemon now explicitly signals the end of its response:

    conn.shutdown(socket.SHUT_WR)

This allows the CLI to exit its receive loop as soon as the response is complete.

---

## First Successful Execution

After these fixes, the system executed end-to-end.

Daemon output during first run:

    [Knowledge] Initializing embedding model and vector store...
    [Knowledge] Initialization complete.
    Hello! I'm NeuroCore...

### Screenshot

![Daemon Initialization](../docs/screenshots/interface/neurocore-daemon-initialization.png)

The CLI timed out on this first run, which is expected due to initialization time.

The important result:

- daemon stayed running  
- system fully initialized  

---

## Second Execution – Warm System

Running the same command again:

    python scripts/ai_cli.py "hello"

Result:

- no initialization  
- immediate response  
- clean output in CLI  

### Screenshot

![CLI Fast Response](../docs/screenshots/interface/neurocore-cli-fast-response.png)

---

## Final System Behavior

### Cold Start

- slow first query (model + vector store initialization)  
- CLI may timeout  
- daemon continues processing  
- system becomes ready  

### Warm State

- no reinitialization  
- fast responses (~1–3 seconds)  
- stable CLI interaction  

---

## Current System Architecture

    CLI
    ↓
    UNIX Socket (/tmp/neurocore.sock)
    ↓
    NeuroCore Daemon
    ↓
    Runtime Manager
    ↓
    Router (logic layer)
    ↓
    Knowledge System (Chroma + embeddings)
    ↓
    LLM (Ollama)
    ↓
    Response

---

## Outcome

NeuroCore now has a working interface layer.

The system is no longer accessed through test scripts.

It can now be used as a command-line AI assistant.

---

## Next Step – Streaming Output

Current behavior:

- daemon streams output locally  
- CLI receives response only after completion  

Next goal:

stream responses directly to the CLI in real time.

Target:

    ai "hello"

with output appearing as it is generated.

---

## Summary

This phase established the first usable interface for NeuroCore.

The system is now:

- persistent  
- stateful  
- accessible from the command line  

This marks the transition from a development system to a usable tool.