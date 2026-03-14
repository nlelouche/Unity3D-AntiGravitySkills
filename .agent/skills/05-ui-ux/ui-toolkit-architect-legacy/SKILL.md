---
name: ui-toolkit-architect
description: "Generates UI Toolkit assets (UXML, USS) and C# Controllers following MVVM. Use when creating "menus", "HUDs", or "interface panels"."
version: 2.0.0
tags: []
argument-hint: panel_name='MainMenu' namespace='Game.UI'
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
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
---

# UI Toolkit Architect

## Overview

## Goal

## When to Use
- Use when defining contracts between systems
- Use when implementing dependency injection
- Use when creating testable code
- Use when menu systems
- Use when UI navigation
To create modern, scalable user interfaces using Unity's **UI Toolkit**. We strictly separate structure (UXML), style (USS), and logic (C# Controller/ViewModel).

## Architecture: MVVM (Model-View-ViewModel)
- **View (UXML/USS)**: The layout and look.
- **Controller (MonoBehaviour)**: Binds the View elements to the ViewModel events.
- **ViewModel (Pure C#)**: Holds the state (e.g., `Score`, `Health`) and Commands.

## Procedure
1.  **Generate Assets**: Create `{Name}.uxml` and `{Name}.uss` in `Assets/UI/{Name}/`.
2.  **Generate Logic**: Create `{Name}Controller.cs` attached to a `UIDocument`.
3.  **Link**: Ensure the Controller knows how to find the buttons defined in UXML (Query by name).

## Few-Shot Example
User: "Create a Pause Menu."
Agent:
1.  Creates `PauseMenu.uxml` with "Resume" and "Quit" buttons.
2.  Creates `PauseMenu.uss` with styling.
3.  Creates `PauseMenuController.cs` that binds `root.Q<Button>("Resume")` to `Time.timeScale = 1`.

## Best Practices
- Follow the patterns and constraints documented in this skill.
- Always run @context-discovery-agent before applying this skill to verify environment compatibility.
- Apply TDD where applicable: write the interface contract first, then implement.
- Zero GC in hot paths: cache references, avoid LINQ and 
ew allocations in Update loops.


---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void UiToolkitArchitectLegacy_Should{ExpectedBehavior}_When{Condition}()
{{
    // Arrange
    // TODO: Setup test fixtures
    
    // Act
    // TODO: Execute system under test
    
    // Assert
    Assert.Fail("Not implemented — write test first");
}}

// Test 2: should handle [edge case]
[Test]
public void UiToolkitArchitectLegacy_ShouldHandle{EdgeCase}()
{{
    // Arrange
    // TODO: Setup edge case scenario
    
    // Act
    // TODO: Execute
    
    // Assert
    Assert.Fail("Not implemented");
}}

// Test 3: should throw when [invalid input]
[Test]
public void UiToolkitArchitectLegacy_ShouldThrow_When{InvalidInput}()
{{
    // Arrange
    var invalidInput = default;
    
    // Act & Assert
    Assert.Throws<Exception>(() => {{ /* execute */ }});
}}
```

### Pasos para completar el TDD:

1. **Descomenta** los tests above
2. **Implementa** la funcionalidad mínima para que compile
3. **Ejecuta** los tests — deben fallar (RED)
4. **Implementa** la funcionalidad real
5. **Verifica** que los tests pasen (GREEN)
6. **Refactorea** manteniendo los tests verdes

---

**Nota**: Este skill fue marcado como `tdd_first: false` durante la auditoría v2.0.1. La sección TDD fue agregada automáticamente pero requiere customización manual para reflejar el comportamiento real del skill.


## Related Skills
- @context-discovery-agent - Verify Unity version and package compatibility before proceeding
- @unified-style-guide - Naming and formatting conventions
- @automated-unit-testing - TDD scaffolding for this skill's components