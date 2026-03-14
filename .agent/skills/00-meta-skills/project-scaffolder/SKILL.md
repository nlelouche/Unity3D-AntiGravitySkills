---
name: project-scaffolder
description: "Generates the initial folder structure, installs essential packages (Manifest), and configures project settings for a fresh Unity project."
version: 2.0.0
tags: ["meta", "setup", "initialization", "scaffold", "automation"]
argument-hint: "preset='3D_Action' OR preset='2D_Mobile'"
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

# Project Scaffolder

## Overview
Deploys a standard directory structure (`_Scripts`, `_Prefabs`, `Arts`) and modifies the `manifest.json` to install core packages like Input System, TextMeshPro, and Cinemachine immediately.

## When to Use
- Use immediately after creating a new Unity Project.
- Use to standardize folder hierarchy across team members.
- Use to install a "Stack" of packages in one go.

## Architecture

The scaffolder runs a script that:
1.  **Creates Folders**: `Assets/_Game`, `Assets/_Game/Scripts`, etc.
2.  **Edits Manifest**: Reads `Packages/manifest.json`, inserts dependencies, saves.
3.  **Creates README**: Adds a project overview.

## Best Practices
- ✅ Underscore core folders (`_Game`) to keep them at the top.
- ✅ Use `AssetDatabase.CreateFolder` to ensure .meta files are generated.
- ✅ Separate ThirdParty assets from own assets.
- ❌ **NEVER** overwrite existing folders without checking.

## Few-Shot Examples

### Example 1: Folder Structure
**User**: "Setup folders."

**Agent**:
```csharp
Directory.CreateDirectory(Application.dataPath + "/_Game");
Directory.CreateDirectory(Application.dataPath + "/_Game/Scripts");
AssetDatabase.Refresh();
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void ProjectScaffolder_Should{ExpectedBehavior}_When{Condition}()
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
public void ProjectScaffolder_ShouldHandle{EdgeCase}()
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
public void ProjectScaffolder_ShouldThrow_When{InvalidInput}()
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
- `@skill-creator` - For creating skills
- `@version-control-git` - For initializing repo
