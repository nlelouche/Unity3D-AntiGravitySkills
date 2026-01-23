---
name: vfx-graph-shuriken
description: Managers for spawning and pooling Particle Systems and VFX Graphs.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Vfx Graph Shuriken

## Goal
Managers for spawning and pooling Particle Systems and VFX Graphs.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/04-visuals-audio/vfx-graph-shuriken/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run vfx-graph-shuriken..."
Agent: execute python script...
