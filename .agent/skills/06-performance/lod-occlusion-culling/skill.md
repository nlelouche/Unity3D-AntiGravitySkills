---
name: lod-occlusion-culling
description: "Setup for LOD Groups and Occlusion Area baking."
version: 1.0.0
tags: []
argument-hint: arg1='value' arg2='value'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Lod Occlusion Culling

## Goal
Setup for LOD Groups and Occlusion Area baking.

## When to Use
- Use when level of detail
- Use when occlusion culling
- Use when rendering optimization

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/06-performance/lod-occlusion-culling/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run lod-occlusion-culling..."
Agent: execute python script...
