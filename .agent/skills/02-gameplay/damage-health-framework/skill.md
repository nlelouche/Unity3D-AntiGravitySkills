---
name: damage-health-framework
description: Implements IDamageable, Health Components, and Damage Types.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Damage Health Framework

## Goal
Implements IDamageable, Health Components, and Damage Types.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/02-gameplay/damage-health-framework/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run damage-health-framework..."
Agent: execute python script...
