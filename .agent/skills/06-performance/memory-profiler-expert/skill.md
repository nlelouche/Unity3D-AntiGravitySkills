---
name: memory-profiler-expert
description: "Unity memory and performance profiling expertise for identifying bottlenecks and optimizing allocations."
version: 1.0.0
tags: ["performance", "profiling", "memory", "GC", "debugging"]
argument-hint: "profile='memory' OR analyze='allocations' target='mobile'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Memory & Performance Profiler Expert

## Overview
Unity profiling expertise for identifying performance bottlenecks, memory leaks, and GC allocation issues. Essential for optimization.

## When to Use
- Use when experiencing frame drops
- Use when memory grows over time
- Use for pre-release optimization
- Use when GC spikes occur
- Use for platform-specific profiling

## Profiling Tools

```
┌─────────────────────────────────────────────────────────────┐
│                   UNITY PROFILER MODULES                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CPU PROFILER           MEMORY PROFILER                     │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Timeline     │      │ Snapshots    │                    │
│  │ Hierarchy    │      │ Diff Compare │                    │
│  │ Raw Samples  │      │ Object Types │                    │
│  └──────────────┘      └──────────────┘                    │
│                                                             │
│  GPU PROFILER           GC ALLOC                           │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Draw Calls   │      │ Per Frame    │                    │
│  │ Batches      │      │ Call Stacks  │                    │
│  │ Fill Rate    │      │ Type Names   │                    │
│  └──────────────┘      └──────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Common Bottlenecks

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **GC Spikes** | Stutters at intervals | Object pooling, cache |
| **Memory Leak** | Memory grows | Release, weak refs |
| **Main Thread** | Low FPS | Jobs, async |
| **Draw Calls** | GPU bound | Batching, atlasing |

## Key Metrics

| Metric | Target (Mobile) | Target (Desktop) |
|--------|:---------------:|:----------------:|
| Frame Time | <16ms (60fps) | <8ms (120fps) |
| GC Alloc/Frame | 0KB | 0KB |
| Draw Calls | <100 | <500 |
| Triangles | <100K | <1M |

## Best Practices
- ✅ Profile on target device
- ✅ Use Development + Profiler builds
- ✅ Take memory snapshots before/after
- ✅ Check GC allocations every frame
- ✅ Use Deep Profile for call stacks
- ❌ **NEVER** profile in Editor only
- ❌ **NEVER** ignore 0.1KB allocations
- ❌ **NEVER** skip mobile profiling

## Few-Shot Examples

### Example 1: Allocation Tracker
**User**: "Find memory allocations."

**Agent**:
```csharp
#if DEVELOPMENT_BUILD || UNITY_EDITOR
public class AllocationTracker : MonoBehaviour
{
    private long _lastTotalMemory;
    private int _allocsPerSecond;
    private float _timer;
    
    private void Update()
    {
        _timer += Time.deltaTime;
        
        long current = GC.GetTotalMemory(false);
        if (current > _lastTotalMemory)
        {
            _allocsPerSecond++;
        }
        _lastTotalMemory = current;
        
        if (_timer >= 1f)
        {
            if (_allocsPerSecond > 10)
            {
                Debug.LogWarning($"High allocations: {_allocsPerSecond}/sec");
            }
            _allocsPerSecond = 0;
            _timer = 0;
        }
    }
}
#endif
```

### Example 2: Frame Time Monitor
**User**: "Display performance stats."

**Agent**:
```csharp
public class PerformanceHUD : MonoBehaviour
{
    private float _deltaTime;
    
    private void Update()
    {
        _deltaTime += (Time.unscaledDeltaTime - _deltaTime) * 0.1f;
    }
    
    private void OnGUI()
    {
        float fps = 1.0f / _deltaTime;
        float ms = _deltaTime * 1000f;
        
        string text = $"{fps:0.} FPS ({ms:0.0}ms)";
        
        var style = new GUIStyle();
        style.fontSize = 24;
        style.normal.textColor = fps < 30 ? Color.red : 
                                  fps < 60 ? Color.yellow : Color.green;
        
        GUI.Label(new Rect(10, 10, 200, 30), text, style);
    }
}
```

### Example 3: Memory Snapshot Comparison
**User**: "Check for memory leaks."

**Agent**:
```
Workflow:
1. Play game to main menu
2. Memory Profiler → Take Snapshot (Baseline)
3. Play through game loop
4. Return to main menu
5. Force GC: System.GC.Collect()
6. Take Snapshot (After)
7. Compare → Look for:
   - New objects not released
   - Growing collections
   - Texture/mesh duplicates
```

## Profiling Checklist
- [ ] Profile on target hardware
- [ ] Check CPU Timeline for spikes
- [ ] Verify 0 GC alloc in Update
- [ ] Monitor memory over 5 minutes
- [ ] Check draw calls and batches
- [ ] Test worst-case scenarios

## Related Skills
- `@object-pooling-system` - Fix GC allocations
- `@mobile-optimization` - Platform limits
- `@lod-occlusion-culling` - Rendering optimization
