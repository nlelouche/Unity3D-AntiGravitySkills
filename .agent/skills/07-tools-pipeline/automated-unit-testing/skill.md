---
name: automated-unit-testing
description: "Generates PlayMode and EditMode tests using NUnit."
version: 1.0.0
tags: []
argument-hint: arg1='value' arg2='value'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Automated Unit Testing

## Goal
Generates PlayMode and EditMode tests using NUnit.

## When to Use
- Use when unit testing
- Use when test automation
- Use when TDD

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/07-tools-pipeline/automated-unit-testing/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run automated-unit-testing..."
Agent: execute python script...
