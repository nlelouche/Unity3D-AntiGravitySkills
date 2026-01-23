---
name: inventory-crafting-logic
description: "Complete inventory system with slot-based storage, item stacking, and recipe-based crafting."
version: 1.0.0
tags: ["gameplay", "inventory", "crafting", "items", "RPG"]
argument-hint: "action='create_item' name='Health Potion' rarity='Common'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
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

## Related Skills
- `@loot-rng-management` - Loot tables and drops
- `@save-load-serialization` - Persisting inventory
- `@scriptableobject-architecture` - SO patterns

## Template Files
- `templates/ItemDataSO.cs.txt` - Item definition
- `templates/InventorySystem.cs.txt` - Storage controller
- `templates/CraftingSystem.cs.txt` - Crafting logic
