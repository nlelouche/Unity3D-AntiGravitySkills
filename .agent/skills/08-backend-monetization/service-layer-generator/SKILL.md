---
name: service-layer-generator
description: "Generates Backend Service interfaces and implementations. Use to "create auth service", "mock network layer", or "add playfab service"."
version: 2.0.0
tags: []
argument-hint: service_name='AuthService' namespace='Game.Services'
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
  gc_alloc_per_frame: "N/A - async or editor-only"
  max_update_cost: "N/A"
tdd_first: false
---

# Service Layer Generator

## Overview

## Goal
To decouple game logic from external APIs (PlayFab, Firebase, Custom Backend). We generate an **Interface** (`IService`) and an **Implementation** (`Service`) that can be injected via VContainer.

## When to Use
- Use when defining contracts between systems
- Use when implementing dependency injection
- Use when creating testable code
- Use when PlayFab integration
- Use when backend services

## Architecture
- **Interface**: Defines *what* the service does.
- **Implementation**: Defines *how* (REST, SDK, Mock).
- **Rule**: Game Logic ONLY talks to the Interface.

## Procedure
1.  **Analyze**: Determine the scope (Auth, Inventory, Leaderboard).
2.  **Generate**: Create `I{Name}.cs` and `{Name}Impl.cs` in `Assets/Scripts/Services/`.
3.  **Suggest**: Remind the user to register this new service using `di-container-manager`.

## Few-Shot Example
User: "Create a Login Service."
Agent:
1.  Generates `ILoginService.cs` (Methods: `LoginAsync`, `Logout`).
2.  Generates `MockLoginService.cs` (Fake success after 1 second).
3.  User can then swap Mock for Real implementation later.

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