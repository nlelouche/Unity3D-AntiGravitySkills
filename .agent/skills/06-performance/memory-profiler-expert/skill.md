---
name: memory-profiler-expert
description: "Tools to track texture usage and heap allocation."
version: 1.0.0
tags: []
argument-hint: arg1='value' arg2='value'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Memory Profiler Expert

## Goal
Tools to track texture usage and heap allocation.

## When to Use
- Use when performance analysis
- Use when memory debugging
- Use when frame timing

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/06-performance/memory-profiler-expert/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run memory-profiler-expert..."
Agent: execute python script...
