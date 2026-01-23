---
name: grid-based-building-system
description: "Robust grid placement system for city builders and RTS games. Handles snapping, collision checks, rotation, and cost validation."
version: 1.0.0
tags: ["building", "grid", "city-builder", "placement", "rts"]
argument-hint: "mode='Build' prefab='Tower' OR action='Rotate'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Grid-Based Building System

## Overview
Calculates discrete grid coordinates from mouse position for placing objects. Ensures valid placement preventing overlaps and checking resources costs.

## When to Use
- Use for City Builders (SimCity style)
- Use for Tower Defense placement
- Use for Tile-based map editors
- Use for RTS structure construction
- Use for decorating grid-based interiors

## Core Concepts

| Concept | Description | Formula |
|---------|-------------|---------|
| **Snapping** | Rounding float position to int | `Floor(pos / size) * size` |
| **Occupancy** | Checking if cell is free | `bool IsOccupied[x,y]` |
| **Validation** | Can build here? | `ValidPos && Resources >= Cost` |
| **Rotation** | rotating the footprint | `Swap(width, height)` |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BUILDING PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INPUT SYSTEM             GHOST MANAGER (Visual)            │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ Mouse Raycast  │─────▶│ Move Ghost to Grid Pos    │      │
│  └────────┬───────┘      │ Set Color (Green/Red)     │      │
│           │              └───────────────────────────┘      │
│           │                                                 │
│           ▼                                                 │
│  BUILD MANAGER (Logic)    GRID DATA (Model)                 │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ Check Cost     │      │ Occupancy Map [,]         │      │
│  │ Validate Pos   │◀────▶│ Building References       │      │
│  │ Instantiate    │      └───────────────────────────┘      │
│  └────────────────┘                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Separate the "Ghost" (Visual) from the actual "Building" (Logic).
- ✅ Use `Vector3Int` for all grid coordinates.
- ✅ Store the Grid Data efficiently (Dictionary or 2D Array).
- ✅ Implement "Refund" logic for destruction.
- ❌ **NEVER** use Physics.Raycast for grid occupancy (too slow/unreliable); use data.
- ❌ **NEVER** instantiate the final prefab to check if it fits.

## Few-Shot Examples

### Example 1: Grid Calculation
**User**: "Snap to 2x2 grid."

**Agent**:
```csharp
public Vector3 GetGridPos(Vector3 worldPos, int cellSize)
{
    int x = Mathf.FloorToInt(worldPos.x / cellSize) * cellSize;
    int z = Mathf.FloorToInt(worldPos.z / cellSize) * cellSize;
    return new Vector3(x, 0, z);
}
```

### Example 2: Validation
**User**: "Check if area is free."

**Agent**:
```csharp
public bool CanBuild(Vector2Int origin, Vector2Int size)
{
    // Iterate over footprint
    for (int x = 0; x < size.x; x++)
    {
        for (int y = 0; y < size.y; y++)
        {
            if (_grid[origin.x + x, origin.y + y].IsOccupied)
                return false;
        }
    }
    return true;
}
```

## Related Skills
- `@resource-management-system` - Deduct cost
- `@custom-editor-scripting` - Grid visualization tool
