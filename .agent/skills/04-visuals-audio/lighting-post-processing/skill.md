---
name: lighting-post-processing
description: Manages Render Settings, Light Baking setups, and Post-Process Volumes.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Lighting Post Processing

## Goal
Manages Render Settings, Light Baking setups, and Post-Process Volumes.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/04-visuals-audio/lighting-post-processing/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run lighting-post-processing..."
Agent: execute python script...
