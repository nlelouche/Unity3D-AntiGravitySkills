---
name: canvas-performance
description: "UI performance optimization for both UGUI Canvas and UI Toolkit runtime."
version: 1.0.0
tags: ["UI", "performance", "optimization", "Canvas", "batching"]
argument-hint: "target='Canvas' OR optimization='batching' profiler='true'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# UI Performance Optimization

## Overview
UI performance optimization techniques for Unity Canvas (UGUI) and UI Toolkit. Covers batching, dirty flagging, pooling, and profiling strategies.

## When to Use
- Use when UI causes frame drops
- Use when optimizing mobile UI
- Use when dealing with dynamic content
- Use when profiling identifies UI issues
- Use when building complex interfaces

## Performance Comparison

| Aspect | UGUI | UI Toolkit |
|--------|:----:|:----------:|
| Batch breaking | Common issue | Less prone |
| Dirty rebinding | Canvas rebuild | Element repaint |
| Object overhead | GameObject per element | No GameObjects |
| Memory | Higher | Lower |

## UGUI Canvas Optimization

```
┌─────────────────────────────────────────────────────────────┐
│                   CANVAS HIERARCHY                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BAD (Single Canvas)          GOOD (Split Canvases)        │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │ Canvas           │        │ Canvas (Static)  │          │
│  │  ├─ HUD          │        │  ├─ Background   │          │
│  │  ├─ Health Bar ⚡ │        │  └─ Title        │          │
│  │  ├─ Score      ⚡ │        ├──────────────────┤          │
│  │  ├─ Minimap    ⚡ │        │ Canvas (Dynamic) │          │
│  │  └─ Background   │        │  ├─ Health Bar   │          │
│  └──────────────────┘        │  └─ Score        │          │
│                               └──────────────────┘          │
│  ⚡ = Frequent updates cause full rebuild                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Optimizations

| Optimization | Impact | Technique |
|--------------|:------:|-----------|
| Split canvases | High | Separate dynamic/static |
| Disable Raycast Target | Medium | Uncheck on non-interactive |
| Object pooling | High | Reuse list items |
| Disable invisible | Medium | gameObject.SetActive(false) |
| Avoid layout groups | Medium | Use anchors when possible |
| Cache references | Medium | Don't use GetComponent |

## UI Toolkit Optimizations

| Optimization | Technique |
|--------------|-----------|
| Avoid style changes | Use USS classes |
| Query once | Cache Q<> results |
| Virtual lists | ListView with virtualization |
| Avoid generateVisualContent | Use built-in elements |
| Reduce hierarchy | Flatten when possible |

## Best Practices
- ✅ Split dynamic and static into separate canvases
- ✅ Disable Raycast Target on decorative elements
- ✅ Use object pooling for dynamic lists
- ✅ Profile with UI Profiler module
- ✅ Use UI Toolkit for complex hierarchies
- ❌ **NEVER** animate layout properties
- ❌ **NEVER** use GetComponent in Update
- ❌ **NEVER** enable Raycast on all elements

## Few-Shot Examples

### Example 1: Canvas Splitter
**User**: "Optimize my HUD canvas."

**Agent**:
```
Recommended structure:
1. Canvas_Background (Static)
   - Overlay layer 0
   - Background images, frames
   
2. Canvas_HUD_Dynamic (Nested)
   - Health bar, stamina, score
   - Updates frequently
   
3. Canvas_Minimap (Separate)
   - Render Texture display
   - Updates at lower frequency
   
4. Canvas_Popup (Overlay)
   - Dialogs, notifications
   - Only visible when needed
```

### Example 2: Raycast Optimizer
**User**: "Fix raycast performance."

**Agent**:
```csharp
#if UNITY_EDITOR
[MenuItem("Tools/UI/Optimize Raycasts")]
public static void OptimizeRaycasts()
{
    var graphics = FindObjectsOfType<Graphic>();
    int count = 0;
    
    foreach (var g in graphics)
    {
        // Disable raycast on non-Button, non-Toggle elements
        if (g.GetComponent<Selectable>() == null)
        {
            g.raycastTarget = false;
            count++;
        }
    }
    
    Debug.Log($"Disabled raycast on {count} elements");
}
#endif
```

### Example 3: UI Toolkit Pooled List
**User**: "Efficient scrolling list."

**Agent**:
```csharp
// UI Toolkit ListView with virtualization (built-in)
var listView = new ListView(
    itemsSource: _items,
    itemHeight: 50,
    makeItem: () => new ItemView(),
    bindItem: (element, index) => 
    {
        var view = (ItemView)element;
        view.Bind(_items[index]);
    }
);

// Virtualization is automatic - only visible items are created
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
```

## Profiling Tips
- Use **UI Profiler** module
- Check **Canvas.BuildBatch** time
- Watch for **Layout** spikes
- Monitor **Fill rate** on mobile
- Use **Frame Debugger** for batches

## Related Skills
- `@ui-toolkit-modern` - Modern UI approach
- `@responsive-ui-design` - Layout optimization
- `@object-pooling` - Pool patterns
