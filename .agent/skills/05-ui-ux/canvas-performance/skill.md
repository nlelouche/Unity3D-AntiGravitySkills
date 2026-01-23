---
name: canvas-performance
description: Best practices for UGUI optimization (Split Canvases, Raycast Target).
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Canvas Performance

## Goal
Best practices for UGUI optimization (Split Canvases, Raycast Target).

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/05-ui-ux/canvas-performance/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run canvas-performance..."
Agent: execute python script...
