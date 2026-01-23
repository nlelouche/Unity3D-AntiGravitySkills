---
name: ability-skill-system
description: Creates a Data-Driven Ability System using ScriptableObjects for cooldowns, costs, and effects.
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Ability Skill System

## Goal
Creates a Data-Driven Ability System using ScriptableObjects for cooldowns, costs, and effects.

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/02-gameplay/ability-skill-system/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run ability-skill-system..."
Agent: execute python script...
