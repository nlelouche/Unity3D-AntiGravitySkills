---
name: shader-graph-expert
description: Helper for material property block manipulation and shader setup.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Shader Graph Expert

## Goal
Helper for material property block manipulation and shader setup.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/04-visuals-audio/shader-graph-expert/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run shader-graph-expert..."
Agent: execute python script...
