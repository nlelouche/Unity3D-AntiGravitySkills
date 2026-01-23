---
name: lighting-nav-baker
description: "Automation tool for baking static lighting (Lightmaps) and AI Navigation (NavMesh) in one click."
version: 1.0.0
tags: ["lighting", "ai", "bake", "automation", "editor-tools"]
argument-hint: "action='BakeAll' quality='High'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
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

## Related Skills
- `@environment-hazard-system` - NavMesh depends on environment
- `@custom-editor-scripting` - UI for the tool
