---
name: ui-toolkit-architect
description: "Generates UI Toolkit assets (UXML, USS) and C# Controllers following MVVM. Use when creating "menus", "HUDs", or "interface panels"."
version: 2.0.0
tags: []
argument-hint: panel_name='MainMenu' namespace='Game.UI'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
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

# UI Toolkit Architect

## Overview

## Goal

## When to Use
- Use when defining contracts between systems
- Use when implementing dependency injection
- Use when creating testable code
- Use when menu systems
- Use when UI navigation
To create modern, scalable user interfaces using Unity's **UI Toolkit**. We strictly separate structure (UXML), style (USS), and logic (C# Controller/ViewModel).

## Architecture: MVVM (Model-View-ViewModel)
- **View (UXML/USS)**: The layout and look.
- **Controller (MonoBehaviour)**: Binds the View elements to the ViewModel events.
- **ViewModel (Pure C#)**: Holds the state (e.g., `Score`, `Health`) and Commands.

## Procedure
1.  **Generate Assets**: Create `{Name}.uxml` and `{Name}.uss` in `Assets/UI/{Name}/`.
2.  **Generate Logic**: Create `{Name}Controller.cs` attached to a `UIDocument`.
3.  **Link**: Ensure the Controller knows how to find the buttons defined in UXML (Query by name).

## Few-Shot Example
User: "Create a Pause Menu."
Agent:
1.  Creates `PauseMenu.uxml` with "Resume" and "Quit" buttons.
2.  Creates `PauseMenu.uss` with styling.
3.  Creates `PauseMenuController.cs` that binds `root.Q<Button>("Resume")` to `Time.timeScale = 1`.

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