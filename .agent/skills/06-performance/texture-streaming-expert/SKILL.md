---
name: texture-streaming-expert
description: "Manages texture memory via Unity's Mip Streaming system and streaming budget configuration. Prevents VRAM exhaustion on mobile/console by loading only the required mip levels at runtime."
version: 2.0.0
tags: ["performance", "texture", "streaming", "memory", "mip", "vram", "mobile", "optimization"]
argument-hint: "action='configure-budget' budget_mb='256' OR action='audit'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: true
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes (streaming is async on worker threads)"
  max_update_cost: "O(1) — Unity manages streaming queue internally"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - write_to_file
---

# Texture Streaming Expert

## Overview
Unity's **Mip Streaming** system loads only the mip levels that the camera can actually see, dramatically reducing VRAM usage. Instead of loading a 2048×2048 texture fully, it loads the 256×256 mip for distant objects and streams higher mips in as the camera approaches. This is critical for mobile (256MB VRAM budget) and open-world games.

## When to Use
- Use when the **Memory Profiler** shows texture memory exceeding platform budget.
- Use for open-world or large scenes with many high-resolution textures.
- Use when targeting mobile platforms (iOS/Android).
- ❌ Do NOT use for UI textures — they should always be full resolution.
- ❌ Do NOT use for render targets or `RenderTexture` — streaming doesn't apply.

## Core Concepts

| Term | Meaning |
|------|---------|
| **Mip level** | Lower-res version of a texture (mip 0 = full res, mip N = smallest) |
| **Streaming Budget** | Max VRAM allocated to streamed textures (MB) |
| **Desired mip** | The mip level the streaming system wants to load based on screen coverage |
| **Loaded mip** | The mip level actually resident in VRAM |

## Configuration

### 1. Enable Mip Streaming (per texture)
```
Texture Import Settings:
  ☑ Streaming Mip Maps
  Priority: 0 (higher = streamed in sooner)
```

### 2. Global Settings (Quality Settings)
```csharp
// Set in Awake or a Bootstrap:
QualitySettings.streamingMipmapsActive      = true;
QualitySettings.streamingMipmapsMemoryBudget = 256f;   // MB
QualitySettings.streamingMipmapsMaxLevelReduction = 3; // Max mips to drop
QualitySettings.streamingMipmapsAddAllCameras = false; // Only main camera
```

### 3. Platform Budgets (Guidelines)

| Platform | Recommended Budget |
|----------|:-----------------:|
| Mobile (Low) | 128 MB |
| Mobile (High) | 256 MB |
| PC Low | 512 MB |
| PC High | 1024 MB |
| Console | 512–1024 MB |

## Profiling & Monitoring

```csharp
// Runtime diagnostic — log streaming state
private void LogStreamingStats()
{
    Debug.Log($"[Mip Streaming] " +
        $"Budget: {Texture.currentTextureMemory / 1048576f:F1}MB / " +
        $"{Texture.desiredTextureMemory / 1048576f:F1}MB desired | " +
        $"Total: {Texture.totalTextureMemory / 1048576f:F1}MB");
}

// Force-load all mips immediately (use for cutscene pre-warming)
private void PreWarmTextures()
{
    Texture.SetStreamingTextureMaterialDebugProperties();
    Streaming.SetPreloadingTextureMipmapCount(5);
}
```

## Texture Import Best Practices

```
☐ Set "Max Size" based on actual display size (not always 2048!)
☐ Use "Crunch Compression" for large non-normal-map textures
☐ Enable "Generate Mip Maps" on all world-space textures
☐ Disable "Generate Mip Maps" for UI sprites and render targets
☐ Set streaming Priority = 2 for character textures (high priority)
☐ Set streaming Priority = 0 for distant environment textures
```

## Automation: TextureAudit Editor Tool

```csharp
#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

public static class TextureAuditTool
{
    [MenuItem("AntiGravity/Texture Audit")]
    public static void RunAudit()
    {
        var textures = AssetDatabase.FindAssets("t:Texture2D");
        int issues = 0;

        foreach (var guid in textures)
        {
            var path = AssetDatabase.GUIDToAssetPath(guid);
            var importer = (TextureImporter)AssetImporter.GetAtPath(path);
            if (importer == null) continue;

            if (!importer.streamingMipmaps && importer.textureType == TextureImporterType.Default)
            {
                Debug.LogWarning($"[TextureAudit] Streaming disabled: {path}");
                issues++;
            }
        }

        Debug.Log($"[TextureAudit] Found {issues} textures with streaming disabled.");
    }
}
#endif
```

## Best Practices

- ✅ Enable streaming on ALL world-space textures via Import Settings.
- ✅ Set platform-appropriate budget in `QualitySettings` per quality level.
- ✅ Use the `Texture Streaming` view in the Scene View (top-left dropdown) to visualize.
- ✅ Pre-warm critical textures before cutscenes or boss fights.
- ❌ **NEVER** enable streaming on UI atlases — causes visible pop-in.
- ❌ **NEVER** set budget below `currentTextureMemory` — forces constant eviction thrash.



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void TextureStreamingExpert_Should{ExpectedBehavior}_When{Condition}()
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
public void TextureStreamingExpert_ShouldHandle{EdgeCase}()
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
public void TextureStreamingExpert_ShouldThrow_When{InvalidInput}()
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

- `@memory-profiler-expert` — Measure actual texture memory usage
- `@lod-occlusion-culling` — Complement: reduce geometry + texture cost together
- `@addressables-asset-management` — Load/unload texture atlases per scene
