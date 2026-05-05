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

This is the long-term primary UX direction.

Users should eventually be able to ask natural questions without memorizing commands first.

### Examples

```bash
acli "what's wrong with my system?"
acli "why is disk warning?"
acli "show me only network issues"
acli "what should I check next?"
```

### Purpose

Used for:

- beginner-friendly diagnostics
- homelab troubleshooting
- natural follow-up questions
- reducing command memorization

Important constraint:

Broad fuzzy natural-language routing must not be implemented inside the CLI formatter.

Natural-language routing belongs in:

router → reasoning → control plane

---

## 2. Command Style

Single-command execution for fast diagnostics and normal operational use.

### Examples

```bash
acli system
acli disk
acli memory
acli network
acli logs
```

### Purpose

Used for:

- quick checks
- direct troubleshooting
- normal production and homelab support work
- repeatable admin workflows

---

## 3. Power User Style

Precise command + flag control for advanced users.

### Examples

```bash
acli system --signal disk
acli system --severity WARN
acli system --signal disk --severity WARN
acli --raw system
acli --json system
```

### Purpose

Used for:

- focused diagnostics
- scripted workflows
- machine-readable output
- raw evidence review
- production troubleshooting

---

## 4. Interactive Style

Persistent session for iterative troubleshooting and follow-up questions.

### Example

```bash
acli
```

Then:

```bash
> what is wrong with nginx
> what log did you check
> explain that error
> what would you recommend next
```

### Purpose

Used for:

- deeper investigation
- follow-up clarification
- guided troubleshooting in training environments

---

# Personality Model

Argus uses one command interface, but behavior changes based on the installed distribution context.

This is not a separate system.

It is:

> One Argus interface with different personalities

Same capabilities.  
Same tools.  
Same runtime.  
Different behavior style.

---

## 1. Production Personality

This is the standard Argus behavior for real Linux systems.

Used for:

- SMB environments
- homelabs
- customer systems
- operational troubleshooting

### Goal

Help the user understand the problem and fix it quickly.

### Behavior

Argus should:

- explain the issue clearly
- state where it looked
- describe what it found
- recommend a fix
- answer follow-up questions

### Tone

- direct
- professional
- efficient
- human-readable

### Output Expectations

Production Argus should provide both:

- conceptual explanation
- practical next steps

That means it may say:

- what the problem is
- why it believes that
- which logs or system areas were checked
- what fix is recommended
- which commands may be used to verify or resolve the issue

### Example Behavior

A good response might include:

- “nginx is failing because the configuration test is not passing”
- “I checked the service status and the recent nginx logs”
- “The failure appears tied to an invalid directive in the config”
- “Review the nginx config test output and correct the invalid line”
- “You can verify with `nginx -t` and then restart the service once the config passes”

Production Argus should be helpful without becoming a teaching system by default.

---

## 2. Training Personality

This behavior exists only when Argus is installed as part of the training environment.

Used for:

- lab scenarios
- guided troubleshooting
- skill development
- scenario coaching

### Goal

Teach the user how to troubleshoot correctly without immediately taking over.

### Behavior

Training Argus should:

- describe symptoms
- recommend where to look
- encourage logical investigation
- let the user work independently first

### Default Posture

Training Argus is passive by default.

It does not interrupt.  
It does not force hints.  
It does not immediately reveal the answer.

Instead, it behaves like:

> A senior administrator mentoring the user through the problem

### Guidance Flow

#### First Response

Training Argus should begin with:

- symptom framing
- likely investigation areas
- suggested commands or places to inspect
- encouragement to think through the system

Example style:

- “The symptom points to a service-level failure”
- “Start by checking the service status and recent logs”
- “Look at what changed between expected behavior and actual behavior”

#### Follow-Up Guidance

If the user asks for more help, Argus becomes more specific.

It may then provide:

- narrower investigation path
- interpretation of errors
- explanation of command results
- stronger hints

#### Full Coaching Mode

If the user appears frustrated, says they give up, or clearly has no path forward, Argus shifts into full coaching.

At that point it should provide:

- step-by-step troubleshooting guidance
- explanation of each step
- reassurance and mentoring tone
- full resolution path
- reasoning behind the fix

This is not just “the answer.”

It should feel like an experienced admin saying:

- what to do
- why to do it
- what to expect
- how to recognize success

---

# Distribution Availability

Personality availability depends on how Argus is installed.

---

## Standalone Argus Install

Available personality:

- production

Not included:

- training personality
- scenario tracking behavior
- lab coaching workflow

---

## Training Environment Install

Available personalities:

- training (default)
- production (optional switch)

This allows a training user to:

- use mentoring behavior by default
- switch to production-style behavior when desired

---

# Command Structure

Commands should support a simple target-first pattern:

```bash
acli <target> <options>
```

Examples:

```bash
acli system
acli disk
acli memory
acli network
acli logs
acli system --signal disk
acli system --severity WARN
acli system --signal disk --severity WARN
```

Quoted natural-language input remains part of the intended interaction model:

```bash
acli "what's wrong with my system?"
acli "why is disk warning?"
```

The exact command alias may vary, but the official Argus-facing command direction is:

```text
acli
```

---

# Input Handling

ACLI must support:

---

## Direct Input

```bash
acli system
acli disk
acli network
```

---

## Natural-Language Input

```bash
acli "what's wrong with my system?"
acli "why is disk warning?"
acli "show me only network issues"
```

Natural-language input should eventually be routed through the proper router / reasoning / control-plane-approved path.

It must not be implemented as hidden guessing inside the CLI formatter.

---

## Interactive Input

```bash
acli
> diagnose nginx
> what did you find
> what should I check next
```

---

## Piped Input

```bash
journalctl -xe | acli
```

Piped input support already exists in the NeuroCore CLI history and should remain part of the ACLI direction.

Future work should build on that capability for natural explanation workflows such as:

```bash
some-command | acli "explain this"
```

This should be treated as diagnostic input for interpretation, not as unmanaged command execution.

---

# Output Requirements

All ACLI output must be:

- structured
- readable
- grounded in real findings
- concise but useful
- able to expose raw evidence when helpful

ACLI output should make a clear distinction between:

- interpreted findings
- recommendations
- supporting raw evidence

Raw evidence is allowed, but it must be presented as verification context, not as an unexplained command dump.

---

## Output Must Include

Where appropriate, output should include:

- issue summary
- severity
- where Argus looked
- what it found
- why the finding matters
- recommended next steps
- supporting raw evidence when requested or useful

---

## Current Phase 6 Output-Control Behavior

Phase 6 output-control behavior is implemented in the current NeuroCore CLI surface and now supports the Argus-facing `acli` command path.

Current supported examples:

```bash
ai "disk"
ai --raw "disk"
ai --summary "disk"
ai --json "disk"

acli system
acli disk
acli memory
acli network
acli logs
acli system --signal disk
acli system --severity WARN
acli system --signal disk --severity WARN
acli --raw system
acli --json system
```

The current implementation remains in:

```text
scripts/ai_cli.py
```

The `acli` command currently points to the shared CLI implementation:

```text
/usr/local/bin/acli -> /mnt/g/ai/projects/neurocore/scripts/ai_cli.py
```

A future distribution-specific implementation may still move or mirror finalized behavior into:

```text
distributions/argus/cli/acli.py
```

---

### Default Concise Output

Default diagnostic output should be concise.

Example:

```bash
acli disk
```

Default output should show:

- title / summary
- severity
- findings
- recommendations
- raw evidence hint when raw evidence exists

Raw evidence should not be dumped by default.

---

### Report Formatting

Current output formatting includes:

- report-style spacing
- consistent indentation
- severity-sorted findings
- finding labels in the form: `[component] [severity]`
- clean separation between findings, recommendations, and raw evidence hints

---

### Raw Evidence Output

Raw evidence must remain available on demand.

Example:

```bash
acli --raw disk
```

Raw mode should show:

- title / summary
- severity
- findings
- recommendations
- supporting raw evidence

This mode exists for verification, deeper inspection, troubleshooting, and trust.

---

### Summary Output

Summary mode supports fast health checks.

Example:

```bash
acli --summary disk
```

Summary mode should show:

- title / summary
- severity
- raw evidence hint when raw evidence exists

It should omit detailed findings, recommendations, and raw evidence.

---

### JSON Output

JSON mode supports machine-readable workflows.

Example:

```bash
acli --json disk
```

JSON mode should print the full structured response returned by NeuroCore.

This preserves automation, testing, scripting, and future model-facing workflows.

JSON output must remain unfiltered even when display filters exist.

---

### Severity Filtering

Severity filtering is display-only.

Example:

```bash
acli system --severity WARN
```

It filters displayed findings by minimum severity while preserving:

- full structured data
- recommendations
- raw evidence
- JSON output
- diagnostic logic

---

### Signal Filtering

Signal filtering is display-only.

Example:

```bash
acli system --signal disk
```

It filters displayed findings by component/signal while preserving:

- full structured data
- recommendations
- raw evidence
- JSON output
- diagnostic logic

---

### Combined Filtering

Severity and signal filters may be combined.

Example:

```bash
acli system --signal disk --severity WARN
```

This allows precise display control without changing the underlying diagnostic result.

---

### Filtered Recommendation Labeling

When filters are active, recommendations remain visible from the full diagnostic result.

Filtered views should label this clearly:

```text
Recommendations from full diagnostic:
```

This avoids implying that recommendations were filtered along with displayed findings.

---

## Raw Evidence Discoverability

When raw evidence exists but is hidden by default, the CLI should provide a copy/paste-ready hint.

Example:

```text
Raw evidence hidden by default.

  - To inspect raw evidence, run: acli --raw "disk"
```

This lets users inspect raw evidence without memorizing flags.

This is preferred over an interactive `y/n` prompt for the current phase because it preserves predictable behavior for:

- piping
- automation
- screenshots
- JSON output
- repeatable CLI workflows

---

## Output Must NOT Be

- raw command dumps without interpretation
- unexplained log blocks
- vague AI-style filler
- generic advice disconnected from findings
- raw evidence presented as a replacement for diagnosis

Argus must never expose raw output without making it understandable.

---

# Capability Expectations

ACLI should expose Argus capabilities such as:

- system summary
- service inspection
- recent error analysis
- log review
- disk usage analysis
- network inspection
- file discovery
- safe config reading

Capability scope is defined by the Argus tool blueprint and tool manifest.

ACLI is the interface.  
It is not the capability source.

---

# Execution Constraints

ACLI must always respect Argus constraints.

---

## Read-Only Enforcement

ACLI must never:

- modify files
- restart services automatically
- change configuration
- execute destructive commands

---

## Controlled Execution

All system access must:

- pass through the control plane
- use approved tool interfaces
- remain observable
- remain predictable

---

## No Direct System Access

ACLI must not:

- shell out directly outside the tool system
- bypass NeuroCore runtime
- introduce unmanaged execution paths

---

# Question Handling

Users must be able to ask follow-up questions in both personalities.

Examples:

- “What log did you check?”
- “Why do you think that is the issue?”
- “Explain that error in plain English”
- “What should I do next?”
- “Can you walk me through it?”

In production personality, follow-up questions improve clarity and speed.

In training personality, follow-up questions drive mentoring depth.

---

# Relationship to Training System

Inside the training environment, ACLI becomes part of the scenario experience.

It may be used to:

- observe troubleshooting flow
- provide hints
- escalate guidance
- support end-of-scenario review

Training-specific session analysis belongs to the training platform, but ACLI is one of the main user-facing touchpoints.

---

# Future Session Integration

In training environments, ACLI should later support integration with session tracking.

This may include:

- commands executed
- sequence of investigation
- time to resolution
- repeated mistakes
- areas where hints were needed

That data supports:

- performance summaries
- coaching feedback
- future scenario improvement

---

# Relationship to NeuroCore

ACLI does not replace the NeuroCore CLI.

The relationship is:

| Layer | Role |
|------|------|
| NeuroCore | platform |
| Argus | distribution |
| ACLI | user-facing interface for Argus |

The current `ai` command may remain useful as a NeuroCore development command.

The Argus-facing command should be oriented around `acli`.

---

# Final Principle

ACLI should make Argus feel useful immediately.

In production, it should help solve problems quickly with clear insight.

In training, it should behave like a senior admin mentoring the user through real troubleshooting.

It should be easy enough for homelab users to ask natural questions, but powerful enough for advanced users to control output precisely.

Same system.  
Same capabilities.  
Different interaction depth.  
Always controlled.

---

# End of Document