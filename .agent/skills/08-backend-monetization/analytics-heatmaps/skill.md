---
name: analytics-heatmaps
description: "Event tracking wrapper for Unity Analytics or Firebase."
version: 1.0.0
tags: []
argument-hint: arg1='value' arg2='value'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Analytics Heatmaps

## Goal
Event tracking wrapper for Unity Analytics or Firebase.

## When to Use
- Use when implementing decoupled communication
- Use when creating publish-subscribe patterns
- Use when reducing dependencies between systems
- Use when event tracking
- Use when player metrics

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/08-backend-monetization/analytics-heatmaps/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run analytics-heatmaps..."
Agent: execute python script...
