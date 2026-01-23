---
name: shader-graph-expert
description: "Unity Shader Graph specialist for creating custom shaders, materials, and visual effects without code."
version: 1.0.0
tags: ["visuals", "shaders", "Shader-Graph", "materials", "rendering"]
argument-hint: "shader_type='Lit' effect='dissolve' OR property='_MainColor'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Shader Graph Expert

## Overview
Unity Shader Graph for creating custom shaders visually. Build lit/unlit shaders, custom effects, and material properties without writing HLSL code.

## When to Use
- Use when creating custom material effects
- Use when implementing dissolve, hologram, force field effects
- Use when building stylized rendering
- Use when vertex displacement is needed
- Use when creating procedural textures

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SHADER GRAPH                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INPUT NODES          PROCESSING           OUTPUT           │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐      │
│  │ Position │───────▶│  Math    │───────▶│ Vertex   │      │
│  │ Normal   │        │  UV      │        │ Fragment │      │
│  │ UV       │        │  Sample  │        │          │      │
│  │ Time     │        │  Lerp    │        │          │      │
│  │ Color    │        │  Step    │        │          │      │
│  └──────────┘        └──────────┘        └──────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Shader Types

| Type | Use Case |
|------|----------|
| **Lit** | PBR materials with lighting |
| **Unlit** | UI, effects, no lighting |
| **Sprite Lit** | 2D sprites with lighting |
| **Decal** | Surface overlays |
| **Fullscreen** | Post-processing effects |

## Common Effects

| Effect | Key Nodes |
|--------|-----------|
| **Dissolve** | Noise + Step + Alpha Clip |
| **Hologram** | Fresnel + Scanlines + Emission |
| **Force Field** | Intersection + Fresnel + Distortion |
| **Water** | Noise + Normal Map + Refraction |
| **Outline** | Vertex Offset + Inverse Hull |

## Best Practices
- ✅ Use Sub Graphs for reusable node groups
- ✅ Expose properties for material variants
- ✅ Use Keywords for shader variants
- ✅ Preview performance in Scene view
- ✅ Use Gradient nodes for color ramps
- ❌ **NEVER** overuse expensive nodes (Voronoi, expensive math)
- ❌ **NEVER** forget to set precision (Full/Half)
- ❌ **NEVER** ignore GPU instancing compatibility

## Few-Shot Examples

### Example 1: Dissolve Effect
**User**: "Create a dissolve shader."

**Agent**:
```
Nodes needed:
1. Simple Noise (scale: 20)
2. Property: _DissolveAmount (0-1)
3. Step (Edge: DissolveAmount, In: Noise)
4. Connect Step to Alpha
5. Set Alpha Clip Threshold to 0.5
6. Optional: Add edge glow with Smoothstep
```

### Example 2: Hologram Shader
**User**: "Make a hologram material."

**Agent**:
```
1. Fresnel Effect (Power: 3)
2. Multiply with HDR color for rim glow
3. Add scanlines: Frac(UV.y * 100 + Time)
4. Step(0.5, scanlines) for hard lines
5. Multiply rim * scanlines * base color
6. Output to Emission (Unlit shader)
```

### Example 3: Material Properties
**User**: "Expose color and smoothness."

**Agent**:
```
Properties to create:
- _BaseColor (Color, HDR: false)
- _Smoothness (Float, Range 0-1, Default 0.5)
- _Metallic (Float, Range 0-1, Default 0)

Connect to PBR Master node outputs.
```

## Pipeline Compatibility
- **URP**: Full support, use URP shaders
- **HDRP**: Full support, more features
- **Built-in**: Limited, use Amplify Shader instead

## Related Skills
- `@vfx-graph-shuriken` - Particle effects
- `@lighting-post-processing` - Lighting setup
- `@procedural-animation-ik` - Shader-driven animation
