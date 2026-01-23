---
name: localization-specialist
description: "Manages Localization Tables and String Keys."
version: 1.0.0
tags: []
argument-hint: arg1='value' arg2='value'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Localization Specialist

## Goal
Manages Localization Tables and String Keys.

## When to Use
- Use when multi-language support
- Use when translation
- Use when localization

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/07-tools-pipeline/localization-specialist/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run localization-specialist..."
Agent: execute python script...
