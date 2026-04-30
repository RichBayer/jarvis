# How Argus Works

---

## What Argus Actually Does

Argus isn’t just running commands.

It’s a system that pulls real data from your machine, figures out what actually matters, and explains what’s going on in plain English.

If you’ve ever bounced between `df -h`, `free -h`, `ps aux`, and logs just to answer a simple question like:

> “Is something wrong with this system?”

Then you already understand the problem this is solving.

Argus is built to shorten that first stage of troubleshooting — the part where you’re gathering clues, comparing outputs, and trying to decide what actually matters.

---

## Who This Is For

Argus was built for how people actually work.

Small teams without a dedicated sysadmin.  
Startups where engineers wear multiple hats.  
Homelabs and personal servers.  

If you’re comfortable in a terminal but don’t want to spend time stitching together raw output, this is for you.

It’s not trying to replace experience.

It’s trying to help you get to the important information faster.

---

## Safety First — Read-Only by Design

Argus is read-only.

It does not modify files, restart services, change configuration, or execute destructive commands.

Everything it does is limited to inspection and interpretation.

That matters because Argus is designed to be used against real systems. The goal is not to let AI run loose on a machine. The goal is to give you a controlled way to understand what the machine is doing.

---

## The Flow

When you run an Argus command, the request follows one controlled path:

You → CLI → Daemon → Runtime Manager → Control Plane → Execution Engine → Tool → System

That path is important.

The CLI does not execute commands directly.  
The model does not execute commands directly.  
User input does not go straight to the operating system.

Everything goes through NeuroCore’s runtime and control layers first.

---

## How Commands Are Routed

In the current version, Argus uses explicit command routing.

The control plane looks at the first word of the request. If that word matches a known execution keyword, the request is routed to a specific tool.

For example:

- `ai "system"` routes to the system analysis tool
- `ai "summary"` routes to the system summary tool
- `ai "disk"` routes to disk analysis
- `ai "memory"` routes to memory analysis
- `ai "network"` routes to network analysis
- `ai "logs"` routes to log analysis

That mapping is deliberate.

Argus is not guessing which tool to run. It is using controlled routing through the platform.

If a request is not recognized as an execution command, it stays on the reasoning side of the system instead of being treated as a system action.

---

## The Tool Layers

The tool system is where Argus becomes useful.

There are two layers that matter most:

1. system tools  
2. Argus tools  

They have different jobs.

---

## System Tools Collect the Data

System tools are the low-level layer.

Their job is simple: collect real system information and return it in a structured format.

A system tool might collect disk usage, memory usage, process information, network state, or logs.

System tools are narrow on purpose. They are not trying to diagnose the whole machine. They are there to gather reliable signals.

Each system tool returns a structured result with:

- status
- message
- data

The message is for humans.

The data is for Argus.

That separation is a big part of what makes the system useful. Argus tools do not have to scrape messy terminal output and hope they understand it correctly. They consume structured data.

---

## Argus Tools Interpret the Data

Argus tools sit above the system tools.

They do not interact with the operating system directly.

Instead, they use structured data from system tools and turn it into something more useful:

- severity
- findings
- recommendations
- evidence

This is where raw system information becomes diagnostic information.

A disk tool can tell you disk usage.

An Argus disk analysis tool can tell you whether that usage matters.

That difference is the point.

---

## System-Level Analysis

The next step is combining signals.

A real system problem usually does not live neatly inside one command. You may need to look at disk, memory, processes, network, and logs before you understand what is happening.

That is what `system_analysis` starts to do.

Instead of making you run several commands and mentally stitch everything together, Argus builds a system-level view.

Run:

`ai "system"`

And Argus returns a structured view of the machine across multiple areas.

---

## Real Output From Argus

The screenshot below is real terminal output from Argus running against a live system.

It is not mocked.  
It is not a fake demo.  
It is not model-generated text.

This is the deterministic Argus analysis layer doing its job before any model explanation is involved.

![System Analysis Overview](./screenshots/argus_acli_ux/20_system_analysis_overview.png)

---

## Deterministic First — AI Second

This is one of the most important ideas behind Argus.

Argus does not start by dumping raw system output into a model and asking it to figure everything out.

It does the hard part first.

It collects system data, structures it, interprets the signals, and produces findings.

The model layer can then be used for explanation and follow-up, but the foundation is already grounded in real system data.

That makes a huge difference.

AI is good at focused reasoning.

It is not good at being handed a pile of raw output and being told:

> “Read all of this, figure out what matters, explain the problem, and tell me what to fix.”

A simple way to think about it:

> Give AI one block and tell it where to put it, and it gets it right fast.  
> Give it a thousand blocks and ask it to organize everything instantly, and that’s where failure starts.

Argus is designed to handle the blocks first.

Then the model gets a cleaner, narrower problem.

---

## Evidence — Not Just Answers

Argus should not ask you to blindly trust it.

When it reports a finding, it keeps the evidence available.

That means you can see:

- what it found
- why it matters
- what data supported the finding

This matters for trust.

A good diagnostic tool should reduce the work, not hide the system.

Argus is meant to make the system easier to read while still keeping the evidence close enough to verify.

---

## Full System Visibility

NeuroCore was built to avoid black-box behavior.

Requests carry trace context through the system so behavior can be followed across the runtime, control plane, execution engine, and tools.

That is useful during development, but it is also part of the larger design philosophy:

If the system makes a decision, that decision should be visible.

If something runs, the path should be understandable.

If something breaks, debugging should not depend on guessing.

---

## What This Enables

Instead of starting with:

`df -h`, `free -h`, `ps aux`, logs, and a lot of manual comparison

You can start with:

`ai "system"`

And get a structured starting point:

- what looks wrong
- how serious it is
- what to check next
- what evidence supports it

It does not solve every problem for you.

That is not the point.

It gets you to the useful part faster.

---

## Final Thought

This started from frustration.

System tools don’t explain anything.  
AI tools don’t understand real systems.  

Argus is built to close that gap.

Not by replacing Linux knowledge.

Not by pretending the model magically knows your machine.

But by collecting real system data, interpreting it through a controlled tool layer, and making the result readable.

At its core, that’s all it’s doing:

Taking a system that normally requires experience to read…

…and making it understandable.