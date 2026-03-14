---
name: asset-import-pipeline
description: "Automated AssetPostprocessor logic to sanitize and optimize assets (Textures, Models, Audio) upon import."
version: 2.0.0
tags: ["tech-art", "import-settings", "optimization", "automation", "pipeline"]
argument-hint: "action='ForceCompression' type='Texture'"
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

# Asset Import Pipeline

## Overview
Acts as a "gatekeeper" for the project. Automatically applies compression settings, naming conventions, and validation rules when assets are imported. Prevents "4K Texture Bloat" and ensures mobile compatibility.

## When to Use
- Use to enforce "Android/iOS" compression standards automatically.
- Use to disable "Import Materials" on FBX files (prevent mess).
- Use to force "Mono" on 3D sound effects.
- Use to validate asset naming conventions.
- Use to detect duplicates.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   IMPORT PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FILE SYSTEM              ASSET POSTPROCESSOR (Editor)      │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ "Hero.fbx"     │─────▶│ OnPreprocessModel()       │      │
│  │ "Grass.png"    │      │ - Scale Factor: 1.0       │      │
│  └────────────────┘      │ - Import Materials: False │      │
│                          └─────────────┬─────────────┘      │
│                                        │                    │
│                                        ▼                    │
│                           ┌───────────────────────────┐     │
│                           │ OnPostprocessTexture()    │     │
│                           │ - Android: ASTC 6x6       │     │
│                           │ - iOS: ASTC 6x6           │     │
│                           │ - PC: BC7                 │     │
│                           └───────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Segregate rules by folder (e.g., `_UI/` vs `_3D/`).
- ✅ Use `AssetPostprocessor` (native Unity API).
- ✅ Detect Normal Maps by suffix (`_Normal`, `_N`) and set TextureType automatically.
- ✅ Log warnings if an asset exceeds size limits (e.g., > 2048px).
- ❌ **NEVER** modify source assets; only import settings.
- ❌ **NEVER** apply heavy compression to UI sprites (artifacts).

## Few-Shot Examples

### Example 1: Texture Rules
**User**: "Compress all textures for mobile."

**Agent**:
```csharp
void OnPreprocessTexture()
{
    TextureImporter importer = (TextureImporter)assetImporter;
    importer.textureCompression = TextureImporterCompression.Compressed;
    // Set platform specific overrides...
}
```

### Example 2: Model Cleanup
**User**: "Don't import materials from FBX."

**Agent**:
```csharp
void OnPreprocessModel()
{
    ModelImporter modelImporter = (ModelImporter)assetImporter;
    modelImporter.materialImportMode = ModelImporterMaterialImportMode.None;
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
public void AssetImportPipeline_Should{ExpectedBehavior}_When{Condition}()
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
public void AssetImportPipeline_ShouldHandle{EdgeCase}()
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
public void AssetImportPipeline_ShouldThrow_When{InvalidInput}()
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
- `@mobile-optimization` - Defines the compression standards
- `@custom-editor-scripting` - Editor API
