---
name: minimap-system
description: "Implements a runtime minimap using a second orthographic camera rendering to a RenderTexture, displayed in a UI Toolkit or UGUI panel. Supports icons, fog of war, and zoom."
version: 2.0.0
tags: ["gameplay", "ui", "minimap", "rendertexture", "camera", "fog-of-war", "hud"]
argument-hint: "style='circular|rectangular' fog_of_war='true|false' zoom='1.0'"
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
  gc_alloc_per_frame: "0 bytes (RenderTexture approach is GPU-driven)"
  max_update_cost: "1 additional camera render pass per frame"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - write_to_file
---

# Minimap System

## Overview
A production minimap uses a **dedicated orthographic camera** positioned directly above the scene, rendering to a **RenderTexture** that is displayed on a UI panel. Icons for entities (player, enemies, objectives) are rendered as **world-space sprites** on a dedicated **Minimap Layer** that only the minimap camera sees. This gives a true real-time rendering with no CPU sampling cost.

## When to Use
- Use for any genre that needs a spatial overview: RPG, RTS, open-world, top-down.
- Use the **UI Toolkit** variant for Unity 6 projects.
- Use the **UGUI (RawImage)** variant for compatibility with older UI setups.
- ❌ Do NOT render every game object directly — use small icon sprites on a dedicated layer.

## Architecture

```
SCENE LAYER: "MinimapIcon"      MINIMAP CAMERA (Orthographic)
┌───────────────────────┐       ┌──────────────────────────────┐
│  Player Icon Sprite   │──────▶│  Culling Mask: MinimapIcon   │
│  Enemy Icon Sprites   │       │  Projection: Orthographic    │
│  Objective Markers    │       │  Output: RenderTexture        │
└───────────────────────┘       └──────────────────────────────┘
                                              │
                                              ▼
                               ┌──────────────────────────────┐
                               │  UI Panel (RawImage/UIT)     │
                               │  Circular mask + zoom        │
                               └──────────────────────────────┘
```

## Setup Procedure

```
☐ 1. Create Layer "MinimapIcon" (Edit → Project Settings → Tags & Layers)
☐ 2. Create Minimap Camera:
      GameObject → Camera
      Set: Projection = Orthographic, Size = 50 (adjust to world scale)
      Set: Culling Mask = MinimapIcon ONLY (uncheck Everything, check MinimapIcon)
      Set: Clear Flags = Solid Color, Background = black
☐ 3. Create RenderTexture (Project → Create → RenderTexture, 256×256)
      Assign to Minimap Camera's "Target Texture"
☐ 4. Create UI Panel:
      UGUI: Add RawImage, drag RenderTexture to Texture field
      UI Toolkit: use background-image in USS
☐ 5. Apply circular mask (UI Toolkit clip-path or UGUI Mask component)
☐ 6. Attach MinimapCameraController to the Camera
```

## Core Implementation

```csharp
// --- MinimapCameraController.cs ---
using UnityEngine;

public class MinimapCameraController : MonoBehaviour
{
    [SerializeField] private Transform _target;      // Player transform
    [SerializeField] private float     _height = 80f;
    [SerializeField] private float     _zoomSize = 50f;

    private Camera _minimapCam;

    private void Awake()
    {
        _minimapCam = GetComponent<Camera>();
        _minimapCam.orthographicSize = _zoomSize;
    }

    private void LateUpdate()
    {
        if (_target == null) return;
        // Follow target, stay at fixed height
        var pos = _target.position;
        transform.position = new Vector3(pos.x, pos.y + _height, pos.z);
    }

    public void SetZoom(float size)
    {
        _zoomSize = Mathf.Clamp(size, 10f, 200f);
        _minimapCam.orthographicSize = _zoomSize;
    }
}

// --- MinimapIcon.cs — attach to any entity that needs a map marker ---
using UnityEngine;

[RequireComponent(typeof(SpriteRenderer))]
public class MinimapIcon : MonoBehaviour
{
    [SerializeField] private Sprite _icon;
    [SerializeField] private Color  _color = Color.white;

    private SpriteRenderer _renderer;

    private void Awake()
    {
        _renderer = GetComponent<SpriteRenderer>();
        _renderer.sprite       = _icon;
        _renderer.color        = _color;
        _renderer.sortingOrder = 100;
        gameObject.layer       = LayerMask.NameToLayer("MinimapIcon");
    }

    // Called when entity dies/despawns
    public void Hide() => gameObject.SetActive(false);
    public void Show() => gameObject.SetActive(true);
}

// --- MinimapIconFactory.cs — spawns icons above entities ---
using UnityEngine;

public class MinimapIconFactory : MonoBehaviour
{
    [SerializeField] private GameObject _iconPrefab;  // Contains MinimapIcon component

    public MinimapIcon CreateFor(Transform entity, Sprite icon, Color color)
    {
        var go   = Instantiate(_iconPrefab, entity);
        go.transform.localPosition = Vector3.up * 2f; // Float above entity
        go.transform.localRotation = Quaternion.Euler(90f, 0f, 0f); // Face camera

        var mi   = go.GetComponent<MinimapIcon>();
        // mi._icon = icon; mi._color = color; (set via serialized fields or method)
        return mi;
    }
}
```

## Fog of War (Optional)

```csharp
// Simple fog-of-war using a second RenderTexture with revealed areas drawn
// via a Shader that unmasks circles around discovered positions.
// Full implementation: use a 512x512 "FogTexture" + update shader via C# API.
// Key shader uniform: _FogTexture (R=explored, G=currently visible)
Shader.SetGlobalTexture("_FogTexture", _fogTexture);
Shader.SetGlobalFloat("_FogStrength", 0.85f);
```

## Best Practices

- ✅ Use a **dedicated Layer** for minimap icons — precise culling control.
- ✅ Set minimap camera **Depth** lower than main camera to render after scene.
- ✅ Scale `orthographicSize` dynamically for zoom-in/out.
- ✅ Parent icon GameObjects to their entity — they move automatically.
- ❌ **NEVER** put terrain/environment meshes on the MinimapIcon layer — massive overhead.
- ❌ **NEVER** use `Camera.main` inside `MinimapCameraController` — keep cameras separate.

## URP Note
In URP, assign the RenderTexture via the Camera's **Output Texture** field in the Universal Additional Camera Data. Ensure the minimap camera is set to **Base** type, not Overlay.



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void MinimapSystem_Should{ExpectedBehavior}_When{Condition}()
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
public void MinimapSystem_ShouldHandle{EdgeCase}()
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
public void MinimapSystem_ShouldThrow_When{InvalidInput}()
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

- `@canvas-performance` — Keep minimap panel in a separate Canvas
- `@procedural-generation` — Render generated dungeon onto minimap
- `@gpu-instancing-expert` — Batch-render many minimap icons if count > 100
