---
name: ui-toolkit-modern
description: "Unity UI Toolkit specialist for professional, scalable, responsive runtime UI with UXML and USS."
version: 2.0.0
tags: ["UI", "UI-Toolkit", "UXML", "USS", "responsive", "modern"]
argument-hint: "component='Button' OR view='MainMenu' binding='playerHealth'"
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
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: false
---

# UI Toolkit Modern

## Overview
Unity UI Toolkit for professional runtime UI. Build scalable, modular, responsive interfaces using UXML (structure), USS (styling), and C# (logic). The modern replacement for UGUI Canvas.

## When to Use
- Use for new projects (Unity 2021+)
- Use for complex, data-driven UI
- Use for multi-platform responsive design
- Use for theming and skinning systems
- Use for professional-grade UI architecture

## UI Toolkit vs UGUI

| Feature | UI Toolkit | UGUI Canvas |
|---------|:----------:|:-----------:|
| Web-like workflow | ✅ | ❌ |
| No GameObjects | ✅ | ❌ |
| Data Binding | ✅ | Manual |
| Styling (USS) | ✅ | Per-element |
| Performance | Better | Good |
| Nested scrolling | ✅ | Complex |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    UI TOOLKIT STACK                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  UXML (Structure)      USS (Styling)      C# (Logic)       │
│  ┌──────────────┐     ┌──────────────┐   ┌──────────────┐  │
│  │ <ui:UXML>    │     │ .button {    │   │ class View { │  │
│  │   <Button>   │────▶│   width: 200;│   │   Query<>()  │  │
│  │   <Label>    │     │   color: #fff│   │   Bind()     │  │
│  │ </ui:UXML>   │     │ }            │   │ }            │  │
│  └──────────────┘     └──────────────┘   └──────────────┘  │
│         │                    │                  │           │
│         └────────────────────┴──────────────────┘           │
│                              │                              │
│                    [UIDocument Component]                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **VisualElement** | Base class for all elements |
| **UIDocument** | MonoBehaviour hosting the UI |
| **UXML** | XML-like markup for structure |
| **USS** | CSS-like styling |
| **UQuery** | Query elements by name/class |
| **Data Binding** | SerializedObject binding |

## Flexbox Layout

```
┌─────────────────────────────────────────┐
│ flex-direction: row                     │
│  ┌─────┐  ┌─────┐  ┌─────┐             │
│  │  1  │  │  2  │  │  3  │             │
│  └─────┘  └─────┘  └─────┘             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ flex-direction: column                  │
│  ┌──────────────────────┐               │
│  │         1            │               │
│  ├──────────────────────┤               │
│  │         2            │               │
│  ├──────────────────────┤               │
│  │         3            │               │
│  └──────────────────────┘               │
└─────────────────────────────────────────┘
```

## Best Practices
- ✅ Use USS classes for reusable styles
- ✅ Query elements once in constructor
- ✅ Use data binding for dynamic content
- ✅ Create reusable components (Custom Controls)
- ✅ Use % and flex for responsive layouts
- ❌ **NEVER** hardcode pixel sizes (use flex)
- ❌ **NEVER** query every frame
- ❌ **NEVER** mix UGUI and UI Toolkit without reason

## Few-Shot Examples

### Example 1: Basic View Controller
**User**: "Create a main menu UI."

**Agent**:
```csharp
public class MainMenuView : MonoBehaviour
{
    [SerializeField] private UIDocument _uiDocument;
    
    private Button _playButton;
    private Button _settingsButton;
    
    private void OnEnable()
    {
        var root = _uiDocument.rootVisualElement;
        
        _playButton = root.Q<Button>("play-button");
        _settingsButton = root.Q<Button>("settings-button");
        
        _playButton.clicked += OnPlayClicked;
        _settingsButton.clicked += OnSettingsClicked;
    }
    
    private void OnDisable()
    {
        _playButton.clicked -= OnPlayClicked;
        _settingsButton.clicked -= OnSettingsClicked;
    }
}
```

### Example 2: UXML Template
**User**: "UXML for a settings panel."

**Agent**:
```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement class="panel settings-panel">
        <ui:Label text="Settings" class="title" />
        
        <ui:VisualElement class="setting-row">
            <ui:Label text="Music Volume" />
            <ui:Slider name="music-slider" low-value="0" high-value="1" />
        </ui:VisualElement>
        
        <ui:VisualElement class="setting-row">
            <ui:Label text="SFX Volume" />
            <ui:Slider name="sfx-slider" low-value="0" high-value="1" />
        </ui:VisualElement>
        
        <ui:Button name="back-button" text="Back" class="btn-secondary" />
    </ui:VisualElement>
</ui:UXML>
```

### Example 3: USS Styling
**User**: "Style for buttons."

**Agent**:
```css
.btn {
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 16px;
    -unity-font-style: bold;
    transition: all 0.2s;
}

.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
    scale: 1.05;
}

.btn-primary:active {
    scale: 0.95;
}
```

## Related Skills
- `@responsive-ui-design` - Multi-device layouts
- `@menu-navigation-flow` - Screen management
- `@input-system-new` - UI navigation input
