---
name: resource-management-system
description: "Economy system for tracking integer-based resources (Gold, Wood, Food) with ScriptableObject keys and event-driven updates."
version: 2.0.0
tags: ["economy", "resources", "inventory", "management", "rts"]
argument-hint: "action='Add' resource='Gold' amount=100"
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

# Resource Management System

## Overview
A data-driven economy system where Resources are defined as `ScriptableObjects`. The Manager holds the inventory (`Dictionary<Resource, int>`) and broadcasts events when values change for UI updates.

## When to Use
- Use for RTS/City Builders (Wood, Stone, Gold)
- Use for RPG Currencies (Gem, Coin, Karma)
- Use for Crafting Ingredients
- Use for tracking ammo or fuel
- Use for validating building costs

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ECONOMY SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESOURCE DATA (Type)     RESOURCE MANAGER (Inventory)      │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ "Gold.asset"   │──────▶ Dictionary<Type, int>     │      │
│  │ "Wood.asset"   │      │ [Gold: 100]               │      │
│  └────────────────┘      │ [Wood: 50]                │      │
│                          └─────────────┬─────────────┘      │
│                                        │                    │
│                                        ▼                    │
│    UI DISPLAY               ┌───────────────────────────┐   │
│  ┌────────────────┐         │ EVENT: OnResourceChanged  │   │
│  │ Update Text()  │◀────────│ (Type, NewValue)          │   │
│  └────────────────┘         └───────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Use `ScriptableObjects` as Keys (prevents string errors like "gold" vs "Gold").
- ✅ Use generic interfaces like `ICost` that accepts `ResourceAmount` structs.
- ✅ Implement `CanAfford()` and `Spend()` helper methods.
- ✅ Separate the UI from the Data (Observer pattern).
- ❌ **NEVER** use Strings as keys (`dict["Gold"]`).
- ❌ **NEVER** update UI in `Update()`; use Events.

## Few-Shot Examples

### Example 1: Defining Resource
**User**: "Create a Wood resource."

**Agent**:
```csharp
[CreateAssetMenu(menuName = "Economy/Resource")]
public class ResourceType : ScriptableObject
{
    public string DisplayName;
    public Sprite Icon;
}
```

### Example 2: Transaction
**User**: "Add 100 wood."

**Agent**:
```csharp
public void AddResource(ResourceType type, int amount)
{
    if (!_inventory.ContainsKey(type)) _inventory[type] = 0;
    
    _inventory[type] += amount;
    OnResourceChanged?.Invoke(type, _inventory[type]);
}
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void ResourceManagementSystem_Should{ExpectedBehavior}_When{Condition}()
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
public void ResourceManagementSystem_ShouldHandle{EdgeCase}()
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
public void ResourceManagementSystem_ShouldThrow_When{InvalidInput}()
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
- `@unity-events-messaging` - Event System
- `@ui-toolkit-modern` - Resource Bar UI
