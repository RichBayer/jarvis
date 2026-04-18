# NeuroCore – Phase 5I Execution Design

---

## Purpose

This phase introduces the first real system-level execution in NeuroCore.

Up to now, everything in the execution layer has been simulated. The architecture is solid, but nothing is actually touching the system yet.

The goal here is simple:

Make execution real, without breaking anything that already works.

---

## Where We Are

NeuroCore already has:

- a control plane that governs all behavior  
- an execution engine that owns tool invocation  
- a tool system with a defined contract  
- full request tracing across the pipeline  

Structurally, execution is already done.

What’s missing is real interaction with the system.

---

## What This Phase Does

This phase adds:

- a safe way for tools to run real system commands  
- the first real read-only tool  
- a foundation we can build more tools on later  

This is not about expanding features.  
It’s about making the execution layer real.

---

## Ground Rules (Do Not Break)

These are already part of the system and must stay true:

- Nothing executes outside the control plane  
- All tools are invoked through the execution engine  
- Tools receive full request objects (not raw strings)  
- Trace continuity is preserved (no new request IDs)  
- Piped input is never executable  

If any of these are broken, the system is no longer valid.

---

## New Component: Command Runner

We will introduce:

```
tools/system/command_runner.py
```

This is a small, focused helper.

Its job:

- run commands safely (`shell=False`)  
- capture stdout / stderr / return codes  
- apply timeouts  
- return structured results  

That’s it.

It does NOT:

- decide what is allowed  
- enforce policy  
- trigger execution  
- handle confirmation  

All authority stays exactly where it already is.

---

## Execution Flow (Updated)

For real tools, the flow becomes:

```
control_plane
→ execution_engine
→ tool
→ command_runner
→ OS
→ tool
→ execution_engine
```

Nothing about the architecture changes.  
The tool layer just becomes real instead of simulated.

---

## First Real Tool

We start with:

```
system_info
```

Planned capabilities:

- hostname  
- uptime  
- OS version  
- kernel  
- CPU info  
- memory  
- disk usage  

This tool is:

- read-only  
- low risk  
- easy to validate  

We are not touching anything state-changing in this phase.

---

## Why Start Here

This lets us prove the entire path works:

- control plane → execution engine → tool → system  

Without introducing risk.

If this works cleanly, everything else builds on top of it.

---

## What We Are NOT Doing (Yet)

This phase does NOT include:

- real service control (start / stop / restart)  
- control plane changes  
- execution policy redesign  
- permissions system  
- Argus-specific behavior  

Those come later.

Right now we’re just establishing a clean foundation.

---

## What We Need To Review First

Before writing any code, we need to look at the real implementation of:

- tools/base_tool.py  
- tools/execution_engine.py  
- tools/tool_registry.py  
- tools/system/service_manager.py  
- runtime/control_plane.py  
- runtime/runtime_manager.py  

We are not modifying anything until we understand exactly how these work.

---

## How We Will Implement This

We’ll move in controlled steps:

1. Review the current tool system  
2. Confirm how tools are registered and invoked  
3. Confirm request structure inside tools  
4. Add command_runner (only if needed based on real code)  
5. Add system_info tool  
6. Register it  
7. Validate execution path end-to-end  
8. Update docs after everything is working  

No shortcuts, no guessing.

---

## Risks To Watch

Main things that could go wrong:

- breaking trace continuity  
- mismatching tool interfaces  
- accidentally bypassing control plane  
- overbuilding too early  

We avoid all of this by inspecting real code first.

---

## Definition of Done

This phase is complete when:

- a real read-only tool runs successfully  
- execution still flows through the control plane  
- execution engine is still the only tool invoker  
- trace continuity is preserved  
- nothing else breaks  

---

## Next Step

Do not write code yet.

Next step is to review the current implementation and align this plan to the real system before making any changes.