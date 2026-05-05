# Argus – ACLI (Argus Command Line Interface) Specification

---

# What This Is

ACLI defines how users interact with Argus.

It is not a separate system.

It is:

> A constrained interface layer that exposes NeuroCore as the Argus distribution

ACLI exists to make Argus usable in real environments while keeping all behavior inside NeuroCore rules.

---

# Core Principle

ACLI does not create new capabilities.

It exposes existing Argus capabilities through a controlled interface.

All behavior still flows through:

daemon → runtime_manager → control_plane

ACLI does not bypass the runtime.  
ACLI does not execute commands directly.  
ACLI does not introduce a parallel system.

---

# Naming

The current Argus-facing command is:

- acli

The existing NeuroCore development command may still be available as:

- ai

User-defined aliases may also exist.

The binary name does not change behavior.

---

# Role of ACLI

ACLI is the user-facing entry point for the Argus distribution.

Its job is to:

- accept user requests
- frame those requests correctly
- route them through NeuroCore
- return structured, human-readable output

ACLI should feel simple to use, but it must remain tightly constrained underneath.

---

# Supported Operation Styles

ACLI supports multiple styles of interaction.

---

## 1. Natural / Fuzzy Style

Primary long-term UX direction.

acli "what's wrong with my system?"  
acli "why is disk warning?"  
acli "what should I check next?"

---

## 2. Command Style

acli system  
acli disk  
acli memory  
acli network  
acli logs  

---

## 3. Power User Style

acli system --signal disk  
acli system --severity WARN  
acli system --signal disk --severity WARN  
acli --raw system  
acli --json system  

---

## 4. Interactive Style

acli  

> what is wrong with nginx  
> what log did you check  
> explain that error  
> what would you recommend next  

---

# Personality Model

(UNCHANGED — intentionally left as-is)

---

# Distribution Availability

(UNCHANGED)

---

# Command Structure

Commands follow a target-first pattern:

acli <target> <options>

Examples:

acli system  
acli disk  
acli memory  
acli network  
acli logs  
acli system --signal disk  
acli system --severity WARN  

Natural language is also supported:

acli "what's wrong with my system?"

---

# Input Handling

ACLI must support:

---

## Direct Input

acli system  
acli disk  

---

## Interactive Input

(UNCHANGED)

---

## Piped Input

journalctl -xe | acli

---

# Output Requirements

(UNCHANGED)

---

## Current Phase 6 Output Behavior

Phase 6 output-control is COMPLETE (Build 027).

Current supported behavior:

acli system  
acli disk  
acli system --signal disk  
acli system --severity WARN  
acli system --signal disk --severity WARN  
acli --raw system  
acli --json system  

---

### Default Output

- concise  
- structured  
- severity + findings + recommendations  
- raw hint only  

---

### Raw Mode

acli --raw system  

Shows full raw evidence.

---

### Summary Mode

acli --summary system  

Shows only high-level state.

---

### JSON Mode

acli --json system  

Returns full structured output.

---

### Severity Filtering

acli system --severity WARN  

Display-only filtering.

---

### Signal Filtering

acli system --signal disk  

Display-only filtering.

---

### Combined Filtering

acli system --signal disk --severity WARN  

---

### Raw Evidence Hint

To inspect raw evidence, run:  
acli --raw "system"

---

## Output Must NOT Be

(UNCHANGED)

---

# Capability Expectations

(UNCHANGED)

---

# Execution Constraints

(UNCHANGED)

---

# Question Handling

(UNCHANGED)

---

# Relationship to Training System

(UNCHANGED)

---

# Future Session Integration

(UNCHANGED)

---

# Relationship to NeuroCore

(UNCHANGED)

---

# Final Principle

ACLI should feel:

- simple first  
- powerful when needed  

It must support:

- natural interaction  
- direct commands  
- precise control  

Same system.  
Same capabilities.  
Multiple interaction styles.  
Always controlled.

---

# End of Document