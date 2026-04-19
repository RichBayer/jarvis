````markdown
# 021 – Argus Tool Layer Initial Implementation

---

# Objective

This phase introduces the Argus tool layer on top of NeuroCore.

The goal was to establish a repeatable pattern for:

- consuming structured system data  
- interpreting real system signals  
- producing prioritized, actionable output  
- remaining fully aligned with the existing execution pipeline  

This marks the transition from a command execution framework to a system capable of structured interpretation.

---

# Starting State

At the start of this phase:

- NeuroCore system tools were fully implemented and operational  
- execution flow was stable and enforced through the control plane  
- CLI interface (`ai`) was functional  
- system tools returned human-readable output only  
- no structured data existed for machine interpretation  
- no Argus layer existed  

Relevant locations:

- `/mnt/g/ai/projects/neurocore/tools/system/`  
- `/mnt/g/ai/projects/neurocore/tools/argus/`  
- `/mnt/g/ai/projects/neurocore/runtime/control_plane.py`  
- `/mnt/g/ai/projects/neurocore/tools/__init__.py`  

Initial Argus tool:

- `/mnt/g/ai/projects/neurocore/tools/argus/system_summary.py`  

---

# Step 1 – Argus Tool Layer Design

Created:

- `/mnt/g/ai/projects/neurocore/docs/design/argus_tool_layer.md`

Defined:

- Argus tools operate as a composition and interpretation layer  
- Argus tools must not call `CommandRunner` directly  
- Argus tools must consume system tools exclusively  
- system tools remain responsible for data collection  
- Argus tools are responsible for interpretation and recommendations  

---

# Step 2 – First Argus Tool Execution

The initial implementation of `system_summary` confirmed that:

- the control plane correctly routed execution  
- the execution engine invoked the Argus tool  
- the tool registry resolved the tool correctly  
- the Argus tool successfully called a system tool  

## Screenshot – First Execution

![First execution of system_summary](../docs/screenshots/argus-system-summary/01_first_execution.png)

This validated the end-to-end execution path.

---

# Step 3 – Initial Parsing Attempt

The next iteration attempted to extract signals from formatted output.

Approach:

- consume system_info output  
- parse using regex  
- extract memory, disk, and load values  

Result:

- partial signal detection  
- inconsistent behavior  
- reliance on fragile formatting assumptions  

## Screenshot – Broken Parsing

![Broken output from early parsing attempt](../docs/screenshots/argus-system-summary/02_broken_output.png)

---

# Step 4 – Controlled Parsing Failure

After tightening parsing logic:

- false positives were eliminated  
- signal detection remained inconsistent  

This confirmed that the issue was not parsing complexity, but data format.

## Screenshot – No Signal Detected

![Controlled failure with no signal extraction](../docs/screenshots/argus-system-summary/03_no_signal_detected.png)

Conclusion:

System tools were returning output optimized for human readability, not machine interpretation.

---

# Step 5 – System Tool Refactor

Updated:

- `/mnt/g/ai/projects/neurocore/tools/system/system_info.py`

Changes:

- preserved CLI output (`message`)  
- added structured `data` field  
- exposed raw command outputs in a consistent format  

Example:

```
{
  "status": "success",
  "message": "...",
  "data": {
    "memory": { "raw": "..." },
    "disk": { "raw": "..." }
  }
}
```

## Screenshot – Structured Output

![Structured raw output from system_info](../docs/screenshots/argus-system-summary/04_system_info_structured_raw.png)

This change enabled reliable machine-level interpretation.

---

# Step 6 – Structured Parsing Implementation

Rewrote `system_summary` to:

- consume `result["data"]`  
- extract values directly  
- eliminate regex-based parsing of formatted text  
- calculate metrics such as memory %, disk %, and load  

## Screenshot – Structured Parsing Success

![Structured parsing success](../docs/screenshots/argus-system-summary/05_structured_parsing_success.png)

This marked the first reliable signal extraction.

---

# Step 7 – Interpretation Layer Upgrade

Enhanced output to include:

- severity levels (OK, WARNING, CRITICAL)  
- prioritized findings  
- conditional recommendations  
- improved formatting  

## Screenshot – Intelligent Summary Baseline

![Intelligent baseline summary](../docs/screenshots/argus-system-summary/06_intelligent_summary.png)

At this stage, the tool produced consistent and meaningful system assessments.

---

# Step 8 – CPU Load Testing

Generated CPU load using:

```
yes > /dev/null &
```

Multiple instances were spawned to observe behavior under increasing load.

## Screenshot – High Load Test

![High load behavior](../docs/screenshots/argus-system-summary/07_high_load_test.png)

Observed:

- correct escalation from OK → WARNING → CRITICAL  
- stable behavior under real system stress  

---

# Step 9 – Load Decay Behavior

After terminating processes:

```
pkill yes
```

Immediately re-evaluated system state.

## Screenshot – Load Still Elevated

![Load decay initial](../docs/screenshots/argus-system-summary/08_load_decay_initial.png)

Observed:

- load remained elevated temporarily  

Reason:

Linux load average is calculated using rolling time windows (1, 5, 15 minutes).

---

# Step 10 – Load Recovery

After a short interval, load returned to normal.

## Screenshot – Load Recovered

![Load decay recovered](../docs/screenshots/argus-system-summary/09_load_decay_recovered.png)

The tool accurately reflected this recovery.

---

# Step 11 – Load Normalization

Adjusted load evaluation to account for CPU count:

- extracted CPU cores from `lscpu`  
- normalized load per core  
- prevented false high-severity classifications on multi-core systems  

---

# Final Result

The `system_summary` tool now:

- consumes structured system data  
- evaluates real system signals  
- assigns severity levels  
- generates actionable recommendations  
- reflects real-world system behavior, including load decay  

Execution remains fully aligned with the existing architecture:

CLI → Control Plane → Execution Engine → Argus Tool → System Tool → OS

---

# Key Outcome

This phase establishes the Argus pattern:

1. Argus tool is selected through normal execution flow  
2. Argus tool calls system tools  
3. system tools return structured data  
4. Argus interprets system state  
5. Argus produces diagnostic output  

This represents a transition from execution-focused tooling to structured system intelligence.

---

# Next Phase

Next tool:

- `process_top`

Goals:

- identify high CPU and memory processes  
- correlate process behavior with system load  
- provide targeted troubleshooting guidance  

With the Argus pattern established, subsequent tools should be significantly faster to implement.

---
````
