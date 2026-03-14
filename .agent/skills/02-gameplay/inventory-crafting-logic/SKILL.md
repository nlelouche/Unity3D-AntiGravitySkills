---
name: inventory-crafting-logic
description: "Complete inventory system with slot-based storage, item stacking, and recipe-based crafting."
version: 2.0.0
tags: ["gameplay", "inventory", "crafting", "items", "RPG"]
argument-hint: "action='create_item' name='Health Potion' rarity='Common'"
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

# Inventory Crafting Logic

## Overview
Complete inventory system with slot-based storage, item stacking, equipment slots, and recipe-based crafting using ScriptableObjects.

## When to Use
- Use when implementing item storage systems
- Use when items need stacking and rarity
- Use when building RPG equipment systems
- Use when implementing crafting mechanics
- Use when building loot/shop systems

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ItemDataSO                              │
│              (ScriptableObject Asset)                       │
├─────────────────────────────────────────────────────────────┤
│  ID, Name, Description, Icon, Rarity                        │
│  Stacking: IsStackable, MaxStackSize                        │
│  Value: BuyPrice, SellPrice                                 │
│  Equipment: EquipSlot, Stats                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  InventorySystem                            │
├─────────────────────────────────────────────────────────────┤
│  InventorySlot[] (Item + Count)                             │
│  AddItem, RemoveItem, HasItem, GetItemCount                 │
│  Events: OnSlotChanged, OnInventoryChanged                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  CraftingSystem                             │
├─────────────────────────────────────────────────────────────┤
│  CraftingRecipeSO[] (Ingredients → Result)                  │
│  CanCraft, TryCraft, GetCraftableRecipes                    │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| `ItemDataSO` | Item definition (stats, rarity, etc.) |
| `InventorySystem` | Slot-based item storage |
| `InventorySlot` | Single slot (item + count) |
| `CraftingSystem` | Recipe-based crafting |
| `CraftingRecipeSO` | Recipe definition |

## Rarity System
| Rarity | Color | Drop Rate |
|--------|-------|-----------|
| Common | Gray/White | ~60% |
| Uncommon | Green | ~25% |
| Rare | Blue | ~10% |
| Epic | Purple | ~4% |
| Legendary | Orange | ~1% |
| Mythic | Red | ~0.1% |

## Best Practices
- ✅ Use ScriptableObjects for item definitions
- ✅ Implement slot events for UI updates
- ✅ Use AddItem return value to check for overflow
- ✅ Store ItemId for save/load, not SO reference
- ❌ **NEVER** modify ItemDataSO at runtime
- ❌ **NEVER** compare items by reference across sessions

## Few-Shot Examples

### Example 1: Add Loot
**User**: "Player picks up a potion."

**Agent**:
```csharp
int overflow = inventory.AddItem(healthPotionSO, 1);
if (overflow > 0)
    Debug.Log("Inventory full!");
```

### Example 2: Check Crafting
**User**: "Can player craft an Iron Sword?"

**Agent**:
```csharp
if (craftingSystem.CanCraft(ironSwordRecipe))
    ShowCraftButton();
else
    ShowMissingIngredients();
```

### Example 3: Equipment Check
**User**: "Equip armor if slot is empty."

**Agent**:
```csharp
if (item.IsEquippable && item.EquipSlot == EquipmentSlot.Chest)
    equipmentSystem.TryEquip(item);
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void InventoryCraftingLogic_Should{ExpectedBehavior}_When{Condition}()
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
public void InventoryCraftingLogic_ShouldHandle{EdgeCase}()
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
public void InventoryCraftingLogic_ShouldThrow_When{InvalidInput}()
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
- `@loot-rng-management` - Loot tables and drops
- `@save-load-serialization` - Persisting inventory
- `@scriptableobject-architecture` - SO patterns

## Template Files
- `templates/ItemDataSO.cs.txt` - Item definition
- `templates/InventorySystem.cs.txt` - Storage controller
- `templates/CraftingSystem.cs.txt` - Crafting logic
