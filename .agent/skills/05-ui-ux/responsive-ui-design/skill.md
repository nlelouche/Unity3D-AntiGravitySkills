---
name: responsive-ui-design
description: Helpers for Anchor/Pivot manipulation and Aspect Ratio Enforcers.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Responsive Ui Design

## Goal
Helpers for Anchor/Pivot manipulation and Aspect Ratio Enforcers.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/05-ui-ux/responsive-ui-design/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run responsive-ui-design..."
Agent: execute python script...
