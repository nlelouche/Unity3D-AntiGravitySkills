---
name: menu-navigation-flow
description: "UI navigation and screen management with stack-based flow, transitions, and history."
version: 1.0.0
tags: ["UI", "navigation", "screens", "stack", "menu"]
argument-hint: "screen='MainMenu' OR action='push' transition='fade'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Menu Navigation & Flow

## Overview
Stack-based UI navigation system for managing screens, modals, and transitions. Supports back button, history, and animated transitions using UI Toolkit.

## When to Use
- Use for multi-screen menu systems
- Use for settings/options hierarchies
- Use for modal dialogs and popups
- Use for back button handling
- Use for screen transitions

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  NAVIGATION ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  NAVIGATION STACK         SCREEN REGISTRY                   │
│  ┌──────────────┐        ┌──────────────┐                  │
│  │ [Audio]  ←── │ Top    │ MainMenu     │                  │
│  │ [Settings]   │        │ Settings     │                  │
│  │ [MainMenu]   │ Base   │ Audio        │                  │
│  └──────────────┘        │ Pause        │                  │
│         ↑                └──────────────┘                  │
│    Push / Pop                                               │
│                                                             │
│  TRANSITIONS: Fade | Slide | Scale | None                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Navigation Types

| Type | Use Case |
|------|----------|
| **Push** | Navigate forward, add to stack |
| **Pop** | Go back, remove from stack |
| **Replace** | Swap current screen |
| **PopToRoot** | Return to first screen |
| **Modal** | Overlay without affecting stack |

## Screen Lifecycle

```
┌─────────────────────────────────────────┐
│            SCREEN LIFECYCLE             │
├─────────────────────────────────────────┤
│                                         │
│  OnInitialize() → OnShow() → OnHide()  │
│                      ↑          │       │
│                      └──────────┘       │
│                  (Back/Forward)         │
│                                         │
│  OnFocus() / OnUnfocus() (stack state) │
│                                         │
└─────────────────────────────────────────┘
```

## Best Practices
- ✅ Use async transitions
- ✅ Cache screen instances (pooling)
- ✅ Handle hardware back button
- ✅ Use transition animations
- ✅ Clear stack on scene change if needed
- ❌ **NEVER** destroy screens on pop (cache them)
- ❌ **NEVER** skip the navigation system
- ❌ **NEVER** block input during transitions

## Few-Shot Examples

### Example 1: Navigation Manager
**User**: "Create a screen navigation system."

**Agent**:
```csharp
public class NavigationManager : MonoBehaviour
{
    [SerializeField] private UIDocument _uiDocument;
    
    private readonly Stack<UIScreen> _screenStack = new();
    private readonly Dictionary<string, UIScreen> _screenCache = new();
    
    public event Action<UIScreen> OnScreenChanged;
    
    public void Push(string screenId)
    {
        if (_screenStack.TryPeek(out var current))
        {
            current.OnUnfocus();
            current.Hide();
        }
        
        var screen = GetOrCreateScreen(screenId);
        _screenStack.Push(screen);
        screen.Show();
        screen.OnFocus();
        
        OnScreenChanged?.Invoke(screen);
    }
    
    public void Pop()
    {
        if (_screenStack.Count <= 1) return;
        
        var current = _screenStack.Pop();
        current.OnUnfocus();
        current.Hide();
        
        var previous = _screenStack.Peek();
        previous.Show();
        previous.OnFocus();
        
        OnScreenChanged?.Invoke(previous);
    }
    
    public void PopToRoot()
    {
        while (_screenStack.Count > 1)
        {
            var screen = _screenStack.Pop();
            screen.Hide();
        }
        
        _screenStack.Peek().Show();
    }
}
```

### Example 2: Base Screen Class
**User**: "Create a base screen class."

**Agent**:
```csharp
public abstract class UIScreen
{
    protected VisualElement Root { get; private set; }
    
    public string ScreenId { get; private set; }
    public bool IsVisible { get; private set; }
    
    public virtual void Initialize(VisualElement root, string screenId)
    {
        Root = root;
        ScreenId = screenId;
        OnInitialize();
    }
    
    protected virtual void OnInitialize() { }
    
    public virtual void Show()
    {
        Root.style.display = DisplayStyle.Flex;
        IsVisible = true;
        OnShow();
    }
    
    public virtual void Hide()
    {
        Root.style.display = DisplayStyle.None;
        IsVisible = false;
        OnHide();
    }
    
    protected virtual void OnShow() { }
    protected virtual void OnHide() { }
    public virtual void OnFocus() { }
    public virtual void OnUnfocus() { }
}
```

### Example 3: Back Button Handler
**User**: "Handle Android back button."

**Agent**:
```csharp
private void Update()
{
    if (Input.GetKeyDown(KeyCode.Escape) || 
        (Gamepad.current?.buttonEast.wasPressedThisFrame ?? false))
    {
        HandleBack();
    }
}

private void HandleBack()
{
    if (_screenStack.Count > 1)
    {
        Pop();
    }
    else
    {
        // At root, show exit confirmation
        ShowExitDialog();
    }
}
```

## Transition Animations
```css
/* Fade transition */
.screen-enter { opacity: 0; }
.screen-enter-active { 
    opacity: 1; 
    transition: opacity 0.3s;
}

/* Slide from right */
.screen-slide-enter { 
    translate: 100% 0; 
}
.screen-slide-enter-active { 
    translate: 0 0; 
    transition: translate 0.3s ease-out;
}
```

## Related Skills
- `@ui-toolkit-modern` - Core UI system
- `@input-system-new` - Navigation input
- `@juice-game-feel` - Transition polish
