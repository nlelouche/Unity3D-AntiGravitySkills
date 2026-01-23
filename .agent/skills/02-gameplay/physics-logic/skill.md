---
name: physics-logic
description: Optimized helper for Raycasts, Overlaps, and LayerMask management.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Physics Logic

## Goal
Optimized helper for Raycasts, Overlaps, and LayerMask management.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/02-gameplay/physics-logic/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run physics-logic..."
Agent: execute python script...
