---
name: status-effect-system
description: "Complete buff/debuff system with stacking, timed effects, tick damage/heal, and stat modifiers."
version: 2.0.0
tags: ["gameplay", "buffs", "debuffs", "status-effects", "RPG"]
argument-hint: "effect_name='Poison' duration='5' tick_damage='10'"
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

# Status Effect System

## Overview
Complete buff/debuff system supporting stacking, duration, tick damage/heal, stat modifiers, and VFX integration.

## When to Use
- Use when implementing buffs (speed boost, damage up)
- Use when implementing debuffs (slow, poison, burn)
- Use when abilities apply status effects
- Use when enemies apply conditions to player
- Use when environmental hazards apply effects

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   StatusEffectSO                            │
│              (ScriptableObject Asset)                       │
├─────────────────────────────────────────────────────────────┤
│  Identity: ID, Name, Icon, Type (Buff/Debuff)               │
│  Duration: Time, IsPermanent, Stacking                      │
│  Tick: Interval, Damage, Heal                               │
│  Stats: [{Stat, Type, Value}, ...]                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                StatusEffectHandler                          │
│              (On Entity)                                    │
├─────────────────────────────────────────────────────────────┤
│  ApplyEffect(effect, stacks)                                │
│  RemoveEffect(effect)                                       │
│  Update: Process ticks, decrement duration                  │
│  Events: OnEffectApplied, OnEffectRemoved, OnEffectTick     │
└─────────────────────────────────────────────────────────────┘
```

## Effect Types

| Type | Examples |
|------|----------|
| **Buff** | Speed Up, Damage Up, Shield |
| **Debuff** | Slow, Poison, Burn, Stun |
| **DoT** | Poison, Burn, Bleed (tick damage) |
| **HoT** | Regeneration (tick heal) |

## Stack Behaviors
- **RefreshDuration**: Reset timer (default)
- **AddDuration**: Extend existing
- **AddStack**: Increase intensity
- **Ignore**: No effect if already applied

## Best Practices
- ✅ Use ScriptableObjects for effect definitions
- ✅ Connect OnEffectTick to damage/heal system
- ✅ Show active effects in UI with duration
- ✅ Use VFX anchor for particle positioning
- ❌ **NEVER** modify StatusEffectSO at runtime
- ❌ **NEVER** forget to integrate tick with health system

## Few-Shot Examples

### Example 1: Apply Poison
**User**: "Enemy attack applies poison."

**Agent**:
```csharp
// In EnemyAttack.cs
if (hit.TryGetComponent<StatusEffectHandler>(out var handler))
{
    handler.ApplyEffect(poisonEffectSO, 1);
}
```

### Example 2: Speed Buff
**User**: "Potion gives 20% speed for 10 seconds."

**Agent**:
```csharp
// StatusEffectSO asset:
// Duration: 10, Type: Buff
// StatModifiers: [{MovementSpeed, Percent, 0.2}]
```

### Example 3: Stacking Bleed
**User**: "Each hit adds a bleed stack, max 5."

**Agent**:
```csharp
// StatusEffectSO asset:
// IsStackable: true, MaxStacks: 5
// StackBehavior: AddStack
// HasTick: true, TickDamage: 5 per stack
```

## Related Skills
- `@damage-health-framework` - Tick damage integration
- `@ability-skill-system` - Abilities that apply effects
- `@scriptableobject-architecture` - SO patterns

## Template Files
- `templates/StatusEffectSO.cs.txt` - Effect definition
- `templates/StatusEffectHandler.cs.txt` - Effect management
