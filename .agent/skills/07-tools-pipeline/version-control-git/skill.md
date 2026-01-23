---
name: version-control-git
description: "Setup for .gitignore and LFS attributes."
version: 1.0.0
tags: []
argument-hint: arg1='value' arg2='value'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Version Control Git

## Goal
Setup for .gitignore and LFS attributes.

## When to Use
- Use when version control
- Use when Git workflow
- Use when branching strategy

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/07-tools-pipeline/version-control-git/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run version-control-git..."
Agent: execute python script...
