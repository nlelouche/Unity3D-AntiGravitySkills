---
name: vfx-graph-shuriken
description: "Unity VFX Graph and Particle System specialist for creating stunning visual effects."
version: 2.0.0
tags: ["visuals", "VFX", "particles", "effects", "Shuriken"]
argument-hint: "effect_type='explosion' OR system='fire' spawn_rate='100'"
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

# VFX Graph & Shuriken

## Overview
Create stunning visual effects using Unity's VFX Graph (GPU) and Shuriken Particle System (CPU). From explosions to ambient particles.

## When to Use
- Use for explosions, fire, smoke, magic
- Use for environmental ambiance (dust, rain, snow)
- Use for UI feedback particles
- Use for trail effects
- Use for impact/hit effects

## System Comparison

| Feature | Shuriken (CPU) | VFX Graph (GPU) |
|---------|:--------------:|:---------------:|
| Particle Count | Thousands | Millions |
| Physics Collisions | ✅ | Limited |
| Complex Behaviors | ✅ | ✅ |
| Performance | Medium | High |
| Ease of Use | Easy | Advanced |
| Min Unity Version | Any | 2019+ |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   SHURIKEN SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│  Main Module → Emission → Shape → Velocity → Color → Size  │
│       ↓                                                     │
│  [Renderer] → Material → Sorting → Trails                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    VFX GRAPH                                │
├─────────────────────────────────────────────────────────────┤
│  Spawn Context → Initialize → Update → Output               │
│       ↓              ↓           ↓          ↓               │
│  [Rate/Burst]   [Position]   [Forces]   [Render]           │
└─────────────────────────────────────────────────────────────┘
```

## Common Effects Library

| Effect | Key Settings |
|--------|--------------|
| **Fire** | Cone shape, Orange→Black color, Noise velocity |
| **Smoke** | Sphere shape, Gray, Size over lifetime ↑, Slow |
| **Explosion** | Burst emission, Sphere shape, Drag, Sub-emitters |
| **Magic Sparkle** | Point shape, HDR colors, Trails, Noise |
| **Blood Splat** | Cone burst, Gravity, Collision, Decal on hit |
| **Rain** | Box shape, Gravity, Stretch, Collision |

## Best Practices
- ✅ Use object pooling for frequently spawned effects
- ✅ Use LOD for distant particle systems
- ✅ Limit collision checks (particle count limit)
- ✅ Use GPU instancing for materials
- ✅ Profile with Particle System window
- ❌ **NEVER** use too many sub-emitters (max 2-3)
- ❌ **NEVER** enable unnecessary modules
- ❌ **NEVER** use world space for moving emitters

## Few-Shot Examples

### Example 1: Explosion
**User**: "Create an explosion effect."

**Agent**:
```
Particle System settings:
- Duration: 0.5s, Looping: false
- Start Lifetime: 0.3-0.5
- Start Speed: 10-20
- Emission: Burst of 50
- Shape: Sphere, Radius 0.5
- Color over Lifetime: Orange → Red → Black
- Size over Lifetime: Large → Small
- Add Sub-emitter for debris
```

### Example 2: Magic Trail
**User**: "Add sparkle trail to projectile."

**Agent**:
```
- Shape: Edge (length 0)
- Emission: Rate over Distance 10
- Trails: Enable, Lifetime 0.5
- Color: HDR cyan glow
- Size: 0.1 → 0
- Renderer: Additive material
```

### Example 3: Ambient Dust
**User**: "Floating dust particles in scene."

**Agent**:
```
- Shape: Box (room size)
- Start Speed: 0.1
- Emission Rate: 20
- Noise: Enable, Strength 0.5
- Color: White, Alpha 0.3
- Size: 0.02-0.05
- Gravity: 0
```

## Performance Tips
- Keep Max Particles reasonable (<1000 for mobile)
- Use Simple collision mode
- Disable unnecessary modules
- Use GPU Instancing
- Pool particle systems



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void VfxGraphShuriken_Should{ExpectedBehavior}_When{Condition}()
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
public void VfxGraphShuriken_ShouldHandle{EdgeCase}()
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
public void VfxGraphShuriken_ShouldThrow_When{InvalidInput}()
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
- `@shader-graph-expert` - Custom particle materials
- `@juice-game-feel` - Impact feedback
- `@lighting-post-processing` - Bloom for particles
