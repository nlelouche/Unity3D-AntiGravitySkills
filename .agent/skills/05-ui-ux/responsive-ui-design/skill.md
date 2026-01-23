---
name: responsive-ui-design
description: "Responsive and adaptive UI design for multi-device support using UI Toolkit flexbox and media queries."
version: 1.0.0
tags: ["UI", "responsive", "adaptive", "mobile", "multi-platform"]
argument-hint: "breakpoint='mobile' OR layout='adaptive' safe_area='true'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Responsive UI Design

## Overview
Responsive and adaptive UI design for Unity. Build interfaces that work across mobile, tablet, desktop, and console using UI Toolkit flexbox, percentage units, and runtime adaptation.

## When to Use
- Use for multi-platform games
- Use for mobile/tablet adaptation
- Use for safe area handling (notches)
- Use for aspect ratio independence
- Use for accessibility scaling

## Responsive Strategies

| Strategy | Description |
|----------|-------------|
| **Fluid** | Percentage-based sizing |
| **Adaptive** | Breakpoint-based layouts |
| **Flexible** | Flexbox grow/shrink |
| **Scalable** | DPI-aware sizing |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               RESPONSIVE UI ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SCREEN SIZE            LAYOUT              SAFE AREA       │
│  ┌──────────┐         ┌──────────┐        ┌──────────┐     │
│  │ Width    │────────▶│ Compact  │───────▶│ Padding  │     │
│  │ Height   │         │ Regular  │        │ Margins  │     │
│  │ DPI      │         │ Expanded │        │ Insets   │     │
│  └──────────┘         └──────────┘        └──────────┘     │
│                                                             │
│  BREAKPOINTS:  Mobile(<600)  Tablet(<1024)  Desktop         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Flexbox Responsive Patterns

| Pattern | USS |
|---------|-----|
| **Fill width** | `width: 100%;` |
| **Grow to fill** | `flex-grow: 1;` |
| **Min constraint** | `min-width: 200px;` |
| **Max constraint** | `max-width: 600px;` |
| **Centered** | `align-self: center;` |

## Safe Area Handling

```
┌─────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← Notch
│                                         │
│   ┌─────────────────────────────────┐   │
│   │                                 │   │
│   │        SAFE CONTENT             │   │
│   │                                 │   │
│   └─────────────────────────────────┘   │
│                                         │
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← Home indicator
└─────────────────────────────────────────┘
```

## Best Practices
- ✅ Use percentage and flex units
- ✅ Handle Screen.safeArea for notches
- ✅ Test on multiple resolutions
- ✅ Use min/max constraints
- ✅ Scale fonts with screen density
- ❌ **NEVER** hardcode pixel positions
- ❌ **NEVER** assume fixed aspect ratio
- ❌ **NEVER** ignore safe areas on mobile

## Few-Shot Examples

### Example 1: Safe Area Handler
**User**: "Handle notch on mobile."

**Agent**:
```csharp
public class SafeAreaHandler : MonoBehaviour
{
    [SerializeField] private UIDocument _uiDocument;
    
    private void OnEnable()
    {
        ApplySafeArea();
    }
    
    private void ApplySafeArea()
    {
        var root = _uiDocument.rootVisualElement;
        var safeArea = Screen.safeArea;
        var screen = new Vector2(Screen.width, Screen.height);
        
        // Convert to percentages
        float left = safeArea.x / screen.x * 100f;
        float right = (screen.x - safeArea.xMax) / screen.x * 100f;
        float top = (screen.y - safeArea.yMax) / screen.y * 100f;
        float bottom = safeArea.y / screen.y * 100f;
        
        var content = root.Q("safe-content");
        content.style.marginLeft = new Length(left, LengthUnit.Percent);
        content.style.marginRight = new Length(right, LengthUnit.Percent);
        content.style.marginTop = new Length(top, LengthUnit.Percent);
        content.style.marginBottom = new Length(bottom, LengthUnit.Percent);
    }
}
```

### Example 2: Responsive Container USS
**User**: "CSS for responsive container."

**Agent**:
```css
.container {
    flex-grow: 1;
    padding: 16px;
    max-width: 1200px;
    align-self: center;
    width: 100%;
}

/* Mobile: full width, smaller padding */
.container.mobile {
    padding: 8px;
    max-width: 100%;
}

/* Tablet: medium constraints */
.container.tablet {
    max-width: 800px;
}
```

### Example 3: Breakpoint Controller
**User**: "Switch layouts based on screen size."

**Agent**:
```csharp
public class ResponsiveController : MonoBehaviour
{
    private VisualElement _root;
    
    private void Update()
    {
        UpdateBreakpoint();
    }
    
    private void UpdateBreakpoint()
    {
        float width = Screen.width;
        
        _root.RemoveFromClassList("mobile");
        _root.RemoveFromClassList("tablet");
        _root.RemoveFromClassList("desktop");
        
        if (width < 600)
            _root.AddToClassList("mobile");
        else if (width < 1024)
            _root.AddToClassList("tablet");
        else
            _root.AddToClassList("desktop");
    }
}
```

## Platform Considerations

| Platform | Focus |
|----------|-------|
| **Mobile** | Touch, safe area, portrait/landscape |
| **Tablet** | Both orientations, larger touch targets |
| **Desktop** | Mouse hover, keyboard navigation |
| **Console** | Gamepad focus, overscan |

## Related Skills
- `@ui-toolkit-modern` - Core UI Toolkit
- `@input-system-new` - Multi-device input
- `@canvas-performance` - Performance optimization
