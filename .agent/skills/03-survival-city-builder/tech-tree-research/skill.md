---
name: tech-tree-research
description: "Generates a Node-based Tech Tree. Use to "unlock upgrades", "research system", or "skill tree UI data"."
version: 1.0.0
tags: []
argument-hint: name='ResearchManager' namespace='Game.Research'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Tech Tree & Research

## Goal
To manage dependencies between upgrades (e.g., "Need Iron Working to unlock Steel").

## When to Use
- Use when research systems
- Use when upgrade trees
- Use when unlock progression

## Architecture
- **TechNode (SO)**: The upgrade data + List of Parent/Child dependencies.
- **TechManager**: Tracks unlocked IDs (HashSet).

## Procedure
1.  **Generate Data**: `TechNode.cs`.
2.  **Generate Logic**: `TechManager.cs`.

## Few-Shot Example
User: "Create a civilization tech tree."
Agent: Generates `TechNode`. "Create nodes for 'Agriculture' and 'Mining'. Set 'Agriculture' as parent of 'Bread'."
