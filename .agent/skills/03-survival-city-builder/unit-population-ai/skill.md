---
name: unit-population-ai
description: Generates lightweight AI for crowds. Use to "manage 100 units", "rts movement", or "population controller".
argument-hint: "name='PopulationManager' namespace='Game.AI'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Unit Population AI

## Goal
To manage large groups of units efficiently, often using a central Manager update loop instead of 1000 Update() calls.

## Architecture
- **UnitManager**: Singleton iterating over a list of `IUnit`.
- **UnitAgent**: Lightweight class/struct.

## Procedure
1.  **Generate Manager**: `PopulationManager.cs`.
2.  **Advice**: Suggest performing logic updates every N frames (Time Slicing).

## Few-Shot Example
User: "Simulate a city crowd."
Agent: Generates `PopulationManager` implementing Time-Sliced updates.
