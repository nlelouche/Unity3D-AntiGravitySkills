---
name: lighting-nav-baker
description: "Automation tool for baking static lighting (Lightmaps) and AI Navigation (NavMesh) in one click."
version: 2.0.0
tags: ["lighting", "ai", "bake", "automation", "editor-tools"]
argument-hint: "action='BakeAll' quality='High'"
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
  check_render_pipeline: true
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
---

# Lighting & Nav Baker

## Overview
A "World Builder" utility that orchestrates the heavy blocking processes of level design. Instead of manually clicking "Bake" on multiple tabs, this skill ensures the environment is fully prepped for gameplay.

## When to Use
- Use after modifying level geometry.
- Use before making a production build.
- Use to enforce lighting quality settings (Draft vs Production).
- Use to rebuild NavMesh Surfaces after moving obstacles.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WORLD BAKER                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BAKE MANAGER (EditorWindow)                                │
│  ┌───────────────────────────┐                              │
│  │ [ Button: BAKE WORLD ]    │                              │
│  └─────────────┬─────────────┘                              │
│                │                                            │
│                ▼                                            │
│  1. CLEAR DATA                                              │
│     - Lightmapping.Clear()                                  │
│     - NavMesh.RemoveAllNavMeshData()                        │
│                │                                            │
│                ▼                                            │
│  2. CONFIGURE                                               │
│     - Set LightSettings (Samples: 1024)                     │
│                │                                            │
│                ▼                                            │
│  3. EXECUTE                                                 │
│     - Lightmapping.BakeAsync()                              │
│     - NavMeshSurface.BuildNavMesh()                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Use `NavMeshSurface` (AI Navigation package) instead of the legacy static baker for runtime flexibility.
- ✅ Always provide a "Clear" option to remove stale data.
- ✅ Run Lighting Bake asynchronously to avoid freezing the Editor UI completely.
- ❌ **NEVER** bake lighting in Play Mode.
- ❌ **NEVER** forget to mark objects as "Static" before baking.

## Few-Shot Examples

### Example 1: NavMesh Bake
**User**: "Rebuild NavMesh."

**Agent**:
```csharp
public void BakeNavMesh()
{
    var surfaces = Object.FindObjectsOfType<NavMeshSurface>();
    foreach(var surface in surfaces) surface.BuildNavMesh();
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
public void LightingNavBaker_Should{ExpectedBehavior}_When{Condition}()
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
public void LightingNavBaker_ShouldHandle{EdgeCase}()
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
public void LightingNavBaker_ShouldThrow_When{InvalidInput}()
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
- `@environment-hazard-system` - NavMesh depends on environment
- `@custom-editor-scripting` - UI for the tool
