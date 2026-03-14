---
name: grid-based-building-system
description: "Robust grid placement system for city builders and RTS games. Handles snapping, collision checks, rotation, and cost validation."
version: 2.0.0
tags: ["building", "grid", "city-builder", "placement", "rts"]
argument-hint: "mode='Build' prefab='Tower' OR action='Rotate'"
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
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
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



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void GridBasedBuildingSystem_Should{ExpectedBehavior}_When{Condition}()
{{
    // Arrange
    // TODO: Setup test fixtures
    
    // Act
    // TODO: Execute system under test
    
    // Assert
    Assert.Fail("Not implemented — write test first");
}}

// Test 2: should handle [edge case]
[Test]
public void GridBasedBuildingSystem_ShouldHandle{EdgeCase}()
{{
    // Arrange
    // TODO: Setup edge case scenario
    
    // Act
    // TODO: Execute
    
    // Assert
    Assert.Fail("Not implemented");
}}

// Test 3: should throw when [invalid input]
[Test]
public void GridBasedBuildingSystem_ShouldThrow_When{InvalidInput}()
{{
    // Arrange
    var invalidInput = default;
    
    // Act & Assert
    Assert.Throws<Exception>(() => {{ /* execute */ }});
}}
```

### Pasos para completar el TDD:

1. **Descomenta** los tests above
2. **Implementa** la funcionalidad mínima para que compile
3. **Ejecuta** los tests — deben fallar (RED)
4. **Implementa** la funcionalidad real
5. **Verifica** que los tests pasen (GREEN)
6. **Refactorea** manteniendo los tests verdes

---

**Nota**: Este skill fue marcado como `tdd_first: false` durante la auditoría v2.0.1. La sección TDD fue agregada automáticamente pero requiere customización manual para reflejar el comportamiento real del skill.


## Related Skills
- `@resource-management-system` - Deduct cost
- `@custom-editor-scripting` - Grid visualization tool
