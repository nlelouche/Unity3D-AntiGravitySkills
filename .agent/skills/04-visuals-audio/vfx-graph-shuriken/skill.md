---
name: vfx-graph-shuriken
description: "Unity VFX Graph and Particle System specialist for creating stunning visual effects."
version: 1.0.0
tags: ["visuals", "VFX", "particles", "effects", "Shuriken"]
argument-hint: "effect_type='explosion' OR system='fire' spawn_rate='100'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
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

## Related Skills
- `@shader-graph-expert` - Custom particle materials
- `@juice-game-feel` - Impact feedback
- `@lighting-post-processing` - Bloom for particles
