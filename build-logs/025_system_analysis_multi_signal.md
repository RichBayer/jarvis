# Build Log 025 – System Analysis Multi-Signal Aggregation and CLI UX

---

## Overview

This phase focused on moving Argus from individual diagnostic commands toward a real **system-level view**.

The previous phases built the foundation. System tools were structured. Argus tools could interpret individual domains. The CLI could route requests through the daemon, runtime manager, control plane, execution engine, and tool layer without bypassing the architecture.

That was important, but it still left a major gap.

The system could answer specific questions like:

> What is disk usage?

or:

> What is memory usage?

But it could not yet answer the question an admin actually cares about first:

> What is the current health of this machine?

That is what this phase started to solve.

The goal was not to add more random commands. The goal was to create a structured diagnostic experience where Argus can look across multiple system domains, surface the most important findings, preserve the raw evidence, and present it in a way that is readable enough for a human but still structured enough for future model reasoning.

---

## The Problem

Before this phase, each diagnostic tool worked on its own.

Disk analysis could identify high disk usage.  
Memory analysis could report memory health.  
Network analysis could inspect interface state.  
Process analysis could detect abnormal CPU or memory usage.

That was useful, but still fragmented.

A user or admin would still need to run several commands, read each output separately, compare the findings manually, and mentally decide what mattered most.

That is exactly the kind of work Argus should eventually reduce.

In a real troubleshooting situation, this matters because time gets wasted switching between commands and interpreting disconnected outputs. The more scattered the information is, the easier it is to miss something obvious. That increases downtime and slows time to resolution.

This phase was about beginning to collapse that friction.

---

## Disk Tool Evolution

The disk tool became the first place where the UX pattern started to take shape.

At first, the output was technically useful, but still too raw. It showed information, but the user had to do the thinking.

### Raw CLI Output

![Disk Raw](../docs/screenshots/argus_acli_ux/01_disk_command_current_cli_output.png)

The next step was making the CLI show the interpretation clearly. Instead of forcing the user to stare at system output and decide what mattered, Argus needed to show the finding directly.

### Structured Output Introduced

![Disk Structured](../docs/screenshots/argus_acli_ux/02_disk_command_structured_output_cleaned.png)

That gave the output a readable shape, but it exposed another important issue.

If Argus only shows the interpretation, the user has to blindly trust it. That is not good enough for a diagnostic tool.

A good admin tool should show what it thinks **and** the evidence it used to reach that conclusion.

### Cleanup Before Raw Integration

![Disk Cleaned](../docs/screenshots/argus_acli_ux/03_disk_command_cleaned_output_before_raw.png)

The fix was to preserve the raw system output and display it underneath the interpretation.

That changed the output from “trust me” to “here is what I found, and here is the proof.”

### Final Output with Raw Evidence

![Disk Final](../docs/screenshots/argus_acli_ux/04_disk_command_final_output_with_real_raw.png)

That distinction is important for the long-term direction of Argus.

Argus should not hide the system from the user. It should reduce the interpretation burden while still keeping the evidence visible.

A user can quickly understand the issue, but an experienced admin can still verify the source data immediately.

---

## Severity Model Added

Once the output became readable, the next issue was clarity around severity.

A label like `WARN` is useful, but only if the user understands the scale. Without context, a warning can feel more severe than it really is, especially if the user does not know that `CRITICAL` exists above it.

So the CLI output was updated to show the severity scale directly:

```text
OK < INFO < WARN < CRITICAL
```

![Disk Severity](../docs/screenshots/argus_acli_ux/05_disk_command_with_severity_scale.png)

This is a small UX detail, but it matters.

It teaches the user how to read the system without requiring a separate manual. It also keeps severity consistent across all tools, which becomes important once multiple signals are combined.

---

## CLI Formatter Layer

After the first formatting pass worked, the next step was separating presentation from logic.

The CLI should be responsible for display.  
The Argus tools should be responsible for interpretation.  
The system tools should be responsible for collecting data.

Keeping those responsibilities separate matters because the CLI will evolve later. It may eventually support filtering, summary mode, raw-output toggles, or different presentation styles. None of that should require changing the diagnostic logic inside the tools.

![CLI Formatter](../docs/screenshots/argus_acli_ux/06_cli_formatter_extracted_no_behavior_change.png)

The formatter was extracted inside the CLI so structured Argus output could be displayed consistently without changing tool behavior.

This created the first version of a real Argus ACLI user experience layer.

---

## Memory Tool Contract Completion

Once disk output was working, memory analysis was used to validate whether the pattern applied cleanly to another domain.

The first test showed that memory output had the interpretation, but not the raw evidence.

### Missing Raw Output

![Memory Missing Raw](../docs/screenshots/argus_acli_ux/07_memory_no_raw_output.png)

That was a contract problem.

For Argus output to be consistent, each tool needs to return the same basic shape:

```text
severity
findings
recommendations
raw
```

Memory already had severity and findings. It needed raw output added so the user could verify the interpretation.

### Raw Output Added

![Memory With Raw](../docs/screenshots/argus_acli_ux/08_memory_with_raw_output.png)

After that, one more consistency issue showed up.

When a tool had no recommendations, the section disappeared. That made the output feel incomplete. It was not clear whether recommendations were intentionally empty or accidentally missing.

The CLI was updated so recommendations are always shown, even when there are none.

### Full Contract Achieved

![Memory Full](../docs/screenshots/argus_acli_ux/09_memory_full_contract_output.png)

That gives every diagnostic output the same structure.

This is useful for humans, but it is even more important for the future model layer. A model will be able to consume this structured diagnostic state without guessing which fields exist.

---

## System Routing Issues

With individual output improving, the next step was introducing a system-level command.

The intended command was:

```bash
ai "system"
```

The first attempt showed that the request was not being routed as an execution request.

### Command Not Routed

![System Not Routed](../docs/screenshots/argus_acli_ux/10_system_command_not_routed.png)

That confirmed the control plane did not yet recognize `system` as a valid execution keyword.

After routing was added, the next issue appeared. The control plane could route the command, but the tool was not registered.

### Tool Not Registered

![Tool Not Registered](../docs/screenshots/argus_acli_ux/11_system_tool_not_registered.png)

This was a good reminder of the full tool path.

For a new Argus tool to work, it must exist, it must be registered, and it must be mapped by the control plane. Missing any one of those pieces breaks the path.

That workflow needs to be documented separately so future tool additions follow the same pattern cleanly.

---

## System Analysis Tool

The new tool introduced in this phase was:

```text
tools/argus/system_analysis.py
```

The purpose of this tool is to aggregate multiple Argus diagnostic tools into one system-level view.

It does not call `CommandRunner` directly.  
It does not bypass the control plane.  
It does not create a new execution path.

It composes existing Argus tools.

The first working version combined disk and memory. That proved the basic pattern, but the raw output was still not presented cleanly.

### Raw Unstructured Output

![System Raw](../docs/screenshots/argus_acli_ux/12_system_analysis_raw_unstructured.png)

The issue was not that data was missing. The issue was that raw evidence was being displayed as internal dictionary structures.

That is not acceptable for the CLI layer. A user should not have to understand Python object formatting to read diagnostic evidence.

The formatter was updated so raw sections were labeled cleanly.

### Clean Output Introduced

![System Clean](../docs/screenshots/argus_acli_ux/13_system_analysis_final_clean_output.png)

At this point, the system had its first clean multi-signal diagnostic output.

That was the real turning point in this phase.

---

## Network Integration

Network analysis was the next signal added to the system view.

Before adding it to `system_analysis`, the individual network tool was tested first. That exposed the same contract gap seen earlier.

### Missing Raw

![Network Missing](../docs/screenshots/argus_acli_ux/14_network_no_raw_output.png)

The tool could interpret interface state, but it did not expose the raw `ip` output.

That needed to be fixed before network could be trusted inside the system-level view.

### Raw Added

![Network Raw](../docs/screenshots/argus_acli_ux/15_network_with_raw_output.png)

Once raw evidence was present, network analysis could be added to `system_analysis`.

### Integrated into System

![System Network](../docs/screenshots/argus_acli_ux/16_system_analysis_with_network.png)

This expanded the system view beyond resource usage.

Now Argus could include connectivity state alongside disk and memory.

A known false positive appeared here: loopback was flagged because its state showed as `UNKNOWN`. That was intentionally left alone for now. This phase was about standardizing structure and aggregation, not tuning every interpretation rule.

---

## Process Analysis

Process analysis was the final signal added during this phase.

The first test showed that process analysis had clean findings and recommendations, but no raw evidence.

### Missing Raw

![Processes Missing](../docs/screenshots/argus_acli_ux/17_processes_no_raw_output.png)

After adding raw handling, another issue appeared.

### Empty Raw

![Processes Empty](../docs/screenshots/argus_acli_ux/18_processes_raw_empty.png)

The raw section existed, but it was empty.

This turned out to be a shape mismatch. The process system tool already returned raw output, but it returned CPU and memory process data separately. The Argus tool was looking for a flat `stdout` field that did not exist.

The fix was to preserve both raw outputs separately:

- CPU sorted process output  
- memory sorted process output  

### Fixed Raw Output

![Processes Final](../docs/screenshots/argus_acli_ux/19_processes_with_raw_output.png)

That completed the evidence pipeline for process diagnostics.

At this point, disk, memory, network, and processes all followed the same diagnostic contract.

---

## Contract Closeout Correction

After the main system-analysis work was completed, a follow-up validation pass found that several implemented Argus tools were working correctly from a routing and interpretation standpoint, but had not yet been aligned with the final raw-evidence diagnostic contract established during this phase.

The affected tools were:

- `tools/argus/connections_analysis.py`
- `tools/argus/uptime_analysis.py`
- `tools/argus/logs_analysis.py`
- `tools/argus/system_summary.py`

These tools already returned the core diagnostic fields:

- severity
- findings
- recommendations

However, they did not consistently expose top-level raw evidence through `data["raw"]` in the same pattern used by the completed diagnostic tools:

- `disk_analysis`
- `memory_analysis`
- `network_analysis`
- `process_top_analysis`
- `system_analysis`

This mattered because the final diagnostic contract is not just about interpretation.

Argus needs to show both:

- what it thinks
- what evidence it used

Without raw evidence, the tools were useful, but they still required the user to trust the interpretation without seeing the supporting system output.

The follow-up correction updated the remaining implemented Argus tools to preserve raw system evidence using the same pattern already established by the completed tools.

This was not new Phase 6 work.

No new execution path was introduced.  
No control-plane behavior was changed.  
No new system intelligence was added.  
No tool bypassed the existing architecture.

This was a contract-alignment cleanup to fully close the Phase 5J diagnostic layer before moving into Distribution Layer work.

---

## Final System Output

With the individual signals cleaned up, they were combined into the final system view.

### Overview

![System Overview](../docs/screenshots/argus_acli_ux/20_system_analysis_overview.png)

This is the main result of the phase.

The command:

```bash
ai "system"
```

now produces one structured diagnostic view containing findings from multiple domains.

Instead of making the user run several commands and manually compare the results, Argus assembles the first layer of system context automatically.

---

### Disk Section

![Disk Section](../docs/screenshots/argus_acli_ux/21_system_analysis_disk_section.png)

---

### Memory Section

![Memory Section](../docs/screenshots/argus_acli_ux/22_system_analysis_memory_section.png)

---

### Network Section

![Network Section](../docs/screenshots/argus_acli_ux/23_system_analysis_network_section.png)

---

### Process Section

![Process Section](../docs/screenshots/argus_acli_ux/24_system_analysis_process_section.png)

Each section keeps the raw evidence visible.

That is important because the tool is not just giving an answer. It is showing how the answer was reached.

---

## What This Enables

This phase creates the foundation for Argus as a useful troubleshooting assistant.

A user or admin can now get an immediate system-health view from one command.

That reduces the amount of time spent gathering basic context.

Instead of starting with:

```bash
df -h
free -h
ip addr
ps aux
```

and manually reading each output, the user can start with:

```bash
ai "system"
```

The system then returns:

- current findings  
- severity  
- recommendations  
- raw evidence  

This can shorten the first stage of troubleshooting significantly.

It does not solve the problem automatically. That is not the point.

It gets the user to the important information faster.

That means faster triage, less time wasted collecting obvious data, and a better chance of reducing downtime.

---

## Future Model Layer

This phase also sets up one of the most important future capabilities.

The structured diagnostic output can later be passed to the model layer.

That matters because the model should not have to scrape raw terminal output and guess what it means. Argus is already doing the deterministic first pass.

The future flow should look like this:

1. System tools collect real machine data  
2. Argus tools structure and interpret that data  
3. `system_analysis` aggregates the current system state  
4. The model receives structured findings, severity, recommendations, and evidence  
5. The model explains the issue in more detail and guides the troubleshooter toward a fix  

This is the direction that makes NeuroCore different from a normal CLI helper.

The model is not starting from nothing.

It receives factual system context that was collected and interpreted through the control-plane governed tool path.

That should make future explanations more grounded, more useful, and less likely to drift.

---

## Operational Impact

This work is directly tied to the long-term Argus ACLI vision.

For an admin, support tech, or small team without deep Linux expertise, the value is simple:

- find issues faster  
- understand severity faster  
- see supporting evidence immediately  
- reduce back-and-forth command gathering  
- improve time to resolution  

This becomes especially useful when paired with the future model layer.

The deterministic layer identifies what is happening.

The model layer can later explain why it matters and how to respond.

That combination is where Argus starts becoming more than a command wrapper.

---

## Observations (Deferred Improvements)

These were identified during the build but intentionally not fixed in this phase.

---

### Network False Positive

Loopback can show as `UNKNOWN`, which currently triggers a warning.

That is a tuning issue in network interpretation logic.

It should be handled later after more network behavior is observed.

---

### Output Size

The system output is already getting large.

That is expected.

This phase prioritized correctness, visibility, and evidence preservation over output control.

Filtering, summary mode, raw toggles, and signal selection should be handled later.

---

### Mixed Severity Findings

The final system view can include both warning-level findings and OK findings.

That is acceptable for now.

Later output control may group findings by severity or suppress OK findings when higher severity issues exist.

---

## System State After This Phase

NeuroCore now has:

- structured CLI diagnostic output  
- consistent Argus tool contracts across core domains  
- raw evidence preserved through the full pipeline  
- system-level aggregation across disk, memory, network, and processes  
- a foundation for model-assisted troubleshooting  

---

## Next Phase

The next phase should focus on output control and signal management.

This includes:

- filtering  
- summarization  
- signal selection  
- raw output controls  
- interpretation refinement  

This is where the output becomes more practical for repeated daily use.

---

## Final Note

This phase started as an effort to make the CLI output easier to read.

It ended up becoming the first real version of system-level diagnosis.

At this point, NeuroCore is no longer just running commands and returning output.

It is beginning to assemble a picture of system health.

That is the foundation Argus needs before it can become a serious troubleshooting tool.