---
name: grid-based-building-system
description: Generates Grid Placement logic. Use to "snap to grid", "building system", or "place furniture".
argument-hint: "name='BuildingManager' namespace='Game.Building'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Grid-Based Building System

## Goal
To translate mouse world-coordinates into discrete Grid coordinates (`Vector3Int`) for placement.

## Core Math
`x = Mathf.FloorToInt(worldPos.x / cellSize) * cellSize`

## Procedure
1.  **Generate Manager**: `BuildingManager.cs` with `Input -> Raycast -> SnapToGrid -> Instantiate` loop.
2.  **Instruction**: Assign a building prefab.

## Few-Shot Example
User: "Allow placing towers on the map."
Agent: Generates `BuildingManager`.
