---
name: virtual-production-lead
description: "Acts as a Project Director. Reads Game Design Documents (GDD), creates production roadmaps, and orchestrates other AntiGravity skills to build the game."
version: 2.0.0
tags: ["meta", "planning", "gdd", "roadmap", "orchestration"]
argument-hint: "action='AnalyzeGDD' path='Design/GDD.md' OR action='GenerateRoadmap'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
  - read_resource
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: false
---

# Virtual Production Lead

## Overview
The "Brain" of the operation. This meta-skill takes a creative Game Design Document (GDD) and translates it into a concrete Engineering Implementation Plan. It identifies which specialized AntiGravity Skills are needed (e.g., "This game needs `horde-wave-logic`" or "This needs `inventory-crafting-logic`") and schedules them.

## When to Use
- Use at the **start of a project** to analyze the GDD.
- Use when **scoping** a new feature request.
- Use to generate a **Milestone/Roadmap** artifact.
- Use to **bootstrap** the initial project structure based on design needs.

## Architecture

The Lead operates in 3 steps:
1.  **Ingestion**: Reads the `GDD.md` (Design).
2.  **Mapping**: Matches features to `SKILL.md` capabilities (Tech Stack).
3.  **Projection**: Generates `task.md` and `implementation_plan.md` (Execution).

## Skill Matrix (Keyword Mapping)

| GDD Keyword | Recommended Skill |
|:---:|:---:|
| "Waves", "Spawner", "Tower Defense" | `@horde-wave-logic` |
| "Health", "Damage", "Armor" | `@damage-health-framework` |
| "Inventory", "Item", "Crafting" | `@inventory-crafting-logic` |
| "Building", "Grid", "Placement" | `@grid-based-building-system` |
| "Hunger", "Thirst", "Cold" | `@environment-hazard-system` |
| "Unlock", "Research", "Tech" | `@tech-tree-research` |
| "Save", "Load", "Persistence" | `@save-load-serialization` |
| "Cutscene", "Camera" | `@cinemachine-specialist` |

## Procedure

1.  **Ask for GDD**: If none exists, provide the `GDD_Template.md`.
2.  **Analyze**: Read the GDD content.
3.  **Generate Plan**: Create a `ProductionRoadmap.md` listing:
    *   **Phase 1: MVP**: Core loops (`@player-movement`, `@camera-system`).
    *   **Phase 2: Systems**: Mechanics (`@inventory`, `@combat`).
    *   **Phase 3: Content**: Levels/AI (`@navmesh-pathfinding`).
4.  **Scaffold**: If requested, run `@project-scaffolder` to set up folders.

## Few-Shot Examples

### Example 1: Full Analysis
**User**: "Here is my GDD for a Zombie Survival game."

**Agent**:
1.  Reads GDD.
2.  Identifies "Zombies" -> `@unit-population-ai`.
3.  Identifies "Survival Stats" -> `@environment-hazard-system`.
4.  Creates `task.md` with specific tasks to implement these skills.

## Templates
- `GDD_Template.md`: Standard Design Doc structure.
- `ProductionRoadmap.md`: Output format.

## Best Practices
- Follow the patterns and constraints documented in this skill.
- Always run @context-discovery-agent before applying this skill to verify environment compatibility.
- Apply TDD where applicable: write the interface contract first, then implement.
- Zero GC in hot paths: cache references, avoid LINQ and 
ew allocations in Update loops.
## Related Skills
- @context-discovery-agent - Verify Unity version and package compatibility before proceeding
- @unified-style-guide - Naming and formatting conventions
- @automated-unit-testing - TDD scaffolding for this skill's components