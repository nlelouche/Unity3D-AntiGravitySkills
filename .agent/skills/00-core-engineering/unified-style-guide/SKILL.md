---
name: unified-style-guide
description: "Establish and enforce a consistent C# coding style for Unity projects. Includes .editorconfig generation and architectural guidelines."
version: 2.0.0
tags: ["style-guide", "csharp", "architecture", ".editorconfig", "best-practices"]
argument-hint: "action='install' OR type='config'"
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

# Unified Style Guide

## Overview
Defines the "North Star" for code quality and consistency. Enforces naming conventions, formatting rules, and architectural standards to ensure the codebase remains maintainable and readable by any team member.

## When to Use
- Use at the **start of a project** to set ground rules.
- Use during **Code Reviews** to cite standards.
- Use when **refactoring** legacy code.
- Use to configure **IDEs** (Rider, VS Code, Visual Studio).
- Use to resolve "Tab vs Space" debates.

## Core Rules

| Category | Rule | Example |
|----------|------|---------|
| **Public Fields** | PascalCase | `public int Health;` |
| **Private Fields** | _camelCase | `private int _currentHealth;` |
| **Methods** | PascalCase | `public void TakeDamage() { }` |
| **Interfaces** | IPrefix | `public interface IDamageable { }` |
| **Classes** | PascalCase | `public class PlayerController : MonoBehaviour` |
| **Serialization** | Force private | `[SerializeField] private int _speed;` |
| **Braces** | Allman (New Line) | `if (true)`<br>`{ ... }` |

## Architecture Standards
1.  **SOLID Principles**: Code should adhere to SOLID where applicable in Unity.
2.  **Composition over Inheritance**: Prefer `GetComponent` and Interfaces over deep class hierarchies.
3.  **Separation of Concerns**: Logic (C#) should be separate from View (Unity UI/Prefab).
4.  **No "Manager" Bloat**: Avoid massive `GameManager.cs` files; break into `ScoreSystem`, `AudioSystem`, etc.

## Best Practices
- ✅ Use `[SerializeField] private` instead of `public` variables.
- ✅ Use `Region` blocks sparingly (only for massive files or interface implementations).
- ✅ Use `namespace` for every script (e.g., `Game.Gameplay.Player`).
- ✅ Remove unused `using` statements.
- ❌ **NEVER** use `GameObject.Find()` in `Update()`.
- ❌ **NEVER** leave empty Unity messages (`Update() {}`) - overhead is non-zero.
- ❌ **NEVER** make fields `public` just to see them in Inspector (use `[SerializeField]`).

## Few-Shot Examples

### Example 1: Installing Config
**User**: "Setup the style guide."

**Agent**:
```bash
# Writes .editorconfig to project root
write_to_file(TargetFile=".editorconfig", Content=TemplateContent...)
```

### Example 2: Code Correction
**User**: "Fix this script style."

**Code (Before)**:
```csharp
public int speed = 10;
void Update() {
    if(speed>5) {
        transform.Translate(0,0,1);
    }
}
```

**Agent (After)**:
```csharp
[SerializeField] private int _speed = 10;

private void Update()
{
    if (_speed > 5)
    {
        transform.Translate(Vector3.forward);
    }
}
```

## Related Skills
- `@automated-unit-testing` - Testing follows style
- `@custom-editor-scripting` - Editor tools style
