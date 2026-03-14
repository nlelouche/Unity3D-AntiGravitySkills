---
name: lod-occlusion-culling
description: "LOD Groups and Occlusion Culling for rendering optimization in 3D environments."
version: 2.0.0
tags: ["performance", "rendering", "LOD", "occlusion", "culling"]
argument-hint: "lod_levels='3' OR occlusion='bake' culling='frustum'"
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
  gc_alloc_per_frame: "0 bytes (target)"
  max_update_cost: "Profiler-verified"
tdd_first: false
---

# LOD & Occlusion Culling

## Overview
Level of Detail (LOD) and Occlusion Culling for rendering optimization. Essential for 3D games with complex environments.

## When to Use
- Use for open world games
- Use for complex 3D environments
- Use when GPU-bound
- Use for mobile 3D games
- Use when many meshes visible

## Culling Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    CULLING PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ALL OBJECTS                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                            │
│  │ FRUSTUM     │── Objects outside camera view → CULLED    │
│  │ CULLING     │                                            │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │ OCCLUSION   │── Objects behind walls → CULLED           │
│  │ CULLING     │                                            │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │ LOD         │── Distant objects → SIMPLIFIED            │
│  │ SELECTION   │                                            │
│  └──────┬──────┘                                            │
│         ▼                                                   │
│     RENDERED                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## LOD Levels

| Level | Distance | Poly Reduction |
|:-----:|:--------:|:--------------:|
| LOD0 | 0-10m | 100% (original) |
| LOD1 | 10-30m | 50% |
| LOD2 | 30-60m | 25% |
| LOD3 | 60m+ | 10% |
| Culled | Far | 0% |

## Culling Types

| Type | Description | Setup |
|------|-------------|-------|
| **Frustum** | Outside camera | Automatic |
| **Occlusion** | Behind occluders | Bake |
| **Distance** | Beyond range | LOD Cull |
| **Layer** | Camera layer mask | Manual |

## Best Practices
- ✅ Bake occlusion for static scenes
- ✅ Use LOD Groups on all meshes
- ✅ Set appropriate LOD distances
- ✅ Mark occluders as Static
- ✅ Use LOD CrossFade
- ❌ **NEVER** skip LOD for small objects
- ❌ **NEVER** use tiny occlusion cells
- ❌ **NEVER** forget to rebake after changes

## Few-Shot Examples

### Example 1: LOD Group Setup
**User**: "Set up LOD for prop."

**Agent**:
```
Unity Setup:
1. Parent object → Add Component → LOD Group
2. Add mesh renderers to each LOD level:
   - LOD0: Full quality mesh
   - LOD1: 50% poly mesh
   - LOD2: 25% poly mesh
   - Culled: Shows nothing

3. Adjust transition percentages:
   - LOD0: 60-100%
   - LOD1: 30-60%
   - LOD2: 10-30%
   - Culled: 0-10%

4. Enable Cross Fade for smooth transitions
```

### Example 2: Occlusion Baking
**User**: "Set up occlusion culling."

**Agent**:
```
Baking workflow:
1. Mark static geometry:
   - Walls, floors → Occluder Static + Occludee Static
   - Props → Occludee Static only
   - Dynamic objects → No static flags

2. Window → Rendering → Occlusion Culling
3. Set parameters:
   - Smallest Occluder: 5 (wall thickness)
   - Smallest Hole: 0.25 (visibility gaps)
   - Backface Threshold: 100

4. Click "Bake"
5. Test with Occlusion visualization
```

### Example 3: Dynamic LOD Controller
**User**: "Adjust LOD bias at runtime."

**Agent**:
```csharp
public class LODController : MonoBehaviour
{
    [SerializeField] private float _highEndBias = 1.0f;
    [SerializeField] private float _lowEndBias = 2.0f;
    
    public void SetQuality(bool highQuality)
    {
        // Higher bias = show lower LODs sooner
        QualitySettings.lodBias = highQuality ? _highEndBias : _lowEndBias;
    }
    
    public void SetMaxLOD(int maxLevel)
    {
        // 0 = show all LODs, 1 = skip LOD0, etc.
        QualitySettings.maximumLODLevel = maxLevel;
    }
}
```

## Occlusion Tips
- Cell size affects bake time and accuracy
- Use Occlusion Areas for indoor areas
- Portals work well for rooms
- Test with Camera preview

## Performance Gains

| Technique | Typical Savings |
|-----------|:---------------:|
| Frustum Culling | 30-50% |
| Occlusion Culling | 20-40% |
| LOD (3 levels) | 50-80% distant |

## Related Skills
- `@mobile-optimization` - Mobile settings
- `@memory-profiler-expert` - Verify gains
- `@shader-graph-expert` - LOD-specific shaders
