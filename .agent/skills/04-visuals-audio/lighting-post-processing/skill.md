---
name: lighting-post-processing
description: "Unity lighting and post-processing specialist for atmosphere, mood, and visual polish."
version: 1.0.0
tags: ["visuals", "lighting", "post-processing", "URP", "HDRP"]
argument-hint: "effect='bloom' intensity='1.5' OR light_type='directional'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Lighting & Post-Processing

## Overview
Unity lighting setup and post-processing effects for atmosphere, mood, and visual polish. Covers URP and HDRP Volume system.

## When to Use
- Use when setting up scene lighting
- Use when adding visual polish (bloom, vignette)
- Use when creating mood/atmosphere
- Use when optimizing lighting for performance
- Use when baking lightmaps

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LIGHTING SETUP                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DIRECT LIGHTS           INDIRECT LIGHT                    │
│  ┌──────────────┐       ┌──────────────┐                   │
│  │ Directional  │       │ Lightmaps    │ (Baked)          │
│  │ Point        │       │ Light Probes │ (Dynamic obj)    │
│  │ Spot         │       │ Reflection   │ (Specular)       │
│  │ Area (Baked) │       │ Probes       │                   │
│  └──────────────┘       └──────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  POST-PROCESSING STACK                      │
├─────────────────────────────────────────────────────────────┤
│  Volume (Global/Local) → Profile → Effects                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │ Bloom  │ │ Color  │ │Vignette│ │ DOF    │ │ Motion │   │
│  │        │ │ Grade  │ │        │ │        │ │ Blur   │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Light Types

| Type | Use Case | Shadows |
|------|----------|:-------:|
| **Directional** | Sun, moon, main light | ✅ |
| **Point** | Lamps, fires, orbs | ✅ |
| **Spot** | Flashlights, spotlights | ✅ |
| **Area** | Soft room lighting | Baked only |

## Post-Processing Effects

| Effect | Impact | Use |
|--------|:------:|-----|
| **Bloom** | Medium | Glow, HDR highlights |
| **Color Grading** | Low | Mood, LUT |
| **Vignette** | Low | Focus, atmosphere |
| **Depth of Field** | High | Focus effect |
| **Motion Blur** | High | Speed feeling |
| **Ambient Occlusion** | High | Contact shadows |
| **Screen Space Reflections** | High | Reflective surfaces |

## Best Practices
- ✅ Use Global Volume for base settings
- ✅ Use Local Volumes for area-specific effects
- ✅ Bake static lighting for performance
- ✅ Use Light Probes for dynamic objects
- ✅ Keep bloom subtle (intensity < 1)
- ❌ **NEVER** use real-time shadows for all lights
- ❌ **NEVER** enable all effects on mobile
- ❌ **NEVER** over-saturate color grading

## Few-Shot Examples

### Example 1: Sunset Mood
**User**: "Create a warm sunset atmosphere."

**Agent**:
```
Directional Light:
- Color: RGB(255, 180, 100)
- Intensity: 1.2
- Rotation: X=15 (low angle)

Volume Profile:
- Color Grading: Warm temperature +20
- Bloom: Intensity 0.5, Threshold 0.9
- Vignette: Intensity 0.3
```

### Example 2: Horror Scene
**User**: "Dark, scary lighting setup."

**Agent**:
```
Lighting:
- Directional: Disabled or very dim
- Point lights: Cold blue, low intensity
- Spot: Harsh white for flashlight

Volume:
- Color Grading: Desaturated, lift shadows blue
- Vignette: 0.4 intensity
- Grain: Enable for film look
- Fog: Volumetric if HDRP
```

### Example 3: Stylized Game
**User**: "Bright, colorful cartoon look."

**Agent**:
```
Lighting:
- Directional: White, Intensity 1.5
- Ambient: Bright gradient sky

Volume:
- No Bloom or subtle
- Color Grading: Boost saturation +10
- No Vignette
- Consider Tonemapping: Neutral
```

## Pipeline Specific
- **URP**: Volume system, limited effects
- **HDRP**: Full feature set, volumetric fog
- **Built-in**: Post Processing Stack v2

## Related Skills
- `@shader-graph-expert` - Custom effects
- `@vfx-graph-shuriken` - Particle bloom interaction
- `@cinemachine-specialist` - Camera DOF
