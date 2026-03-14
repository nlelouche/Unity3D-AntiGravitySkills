---
name: loot-rng-management
description: "Loot table system with weighted drop rates, rarity tiers, and procedural generation."
version: 2.0.0
tags: ["gameplay", "loot", "RNG", "drops", "rewards"]
argument-hint: "loot_table='Chest_Common' guaranteed='false'"
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

# Loot RNG Management

## Overview
Loot table system with weighted random drops, rarity tiers, guaranteed drops, and procedural reward generation.

## When to Use
- Use when enemies drop items on death
- Use when opening chests/containers
- Use when completing quests with random rewards
- Use when gacha/unlock systems are needed
- Use when balancing drop rates

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LootTableSO                              │
│              (ScriptableObject Asset)                       │
├─────────────────────────────────────────────────────────────┤
│  Entries: [{Item, Weight, MinCount, MaxCount}]              │
│  GuaranteedDrops: [ItemDataSO]                              │
│  RollCount: min/max items to roll                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  LootManager.Roll()                         │
├─────────────────────────────────────────────────────────────┤
│  1. Add guaranteed drops                                    │
│  2. Calculate total weight                                  │
│  3. Roll random for each drop slot                          │
│  4. Select item based on weight                             │
│  5. Return List<LootDrop>                                   │
└─────────────────────────────────────────────────────────────┘
```

## Probability System
```
Weight-based probability:
ItemA: Weight 70  → 70/100 = 70%
ItemB: Weight 25  → 25/100 = 25%
ItemC: Weight 5   → 5/100  = 5%
Total: 100
```

## Rarity Modifiers
- Apply luck stat to increase rare drop chance
- Pity system: increase chance after N failures
- Boss multipliers for better loot

## Best Practices
- ✅ Use weights, not percentages (easier to balance)
- ✅ Separate loot tables by source (enemy, chest, boss)
- ✅ Include "nothing" as weighted entry for no-drop
- ✅ Seed RNG for reproducible results in testing
- ❌ **NEVER** modify weights at runtime carelessly
- ❌ **NEVER** forget edge cases (empty table)

## Few-Shot Examples

### Example 1: Enemy Drop
**User**: "Wolf drops leather or meat on death."

**Agent**:
```csharp
// LootTableSO: WolfLoot
// Entries: 
//   - Leather (weight: 60)
//   - Meat (weight: 40)
// RollCount: 1-2

var drops = LootManager.Roll(wolfLootTable);
foreach (var drop in drops)
    SpawnLootPickup(drop.Item, drop.Count);
```

### Example 2: Chest Loot
**User**: "Chest has guaranteed gold + random items."

**Agent**:
```csharp
// LootTableSO: ChestLoot
// GuaranteedDrops: [GoldCoin x 10-50]
// Entries: [Potion, Scroll, Gem] with weights
// RollCount: 2-4
```

### Example 3: Luck Modifier
**User**: "Player luck increases rare drops."

**Agent**:
```csharp
float luckBonus = player.Luck * 0.01f; // +1% per luck
foreach (var entry in entries)
{
    if (entry.Item.Rarity >= ItemRarity.Rare)
        entry.EffectiveWeight *= (1 + luckBonus);
}
```

## Related Skills
- `@inventory-crafting-logic` - Adding drops to inventory
- `@damage-health-framework` - Death triggers loot
- `@scriptableobject-architecture` - Loot table data

## Template Files
Available in templates/ folder.
