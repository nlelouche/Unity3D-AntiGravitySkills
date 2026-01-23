---
name: environment-hazard-system
description: "Implementation of survival mechanics including hunger, thirst, temperature, and atmospheric hazards."
version: 1.0.0
tags: ["survival", "hazards", "environment", "status-effects", "gameplay"]
argument-hint: "feature='Hunger' params='decay_rate=1' OR hazard='radiation_zone'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Environment Hazard System

## Overview
Manages survival statistics (Hunger, Thirst, Oxygen) and environmental hazards (Temperature, Radiation). Features a "Tick" based decay system and zone-based modifiers.

## When to Use
- Use for survival games (Hunger/Thirst)
- Use for underwater sequences (Oxygen)
- Use for hazardous zones (Poison swarms, Lava heat)
- Use for status effects (Buffs/Debuffs)
- Use when implementing death conditions

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   SURVIVAL LOOP                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TICK MANAGER (Global)        PLAYER STATS                  │
│  ┌──────────────────┐        ┌───────────────────────┐      │
│  │ Tick: 1.0s       │───────▶│ Hunger: 100 -> 99     │      │
│  └──────────────────┘        │ Thirst: 100 -> 98     │      │
│                              │ Temp:   37c -> 36c    │      │
│                              └───────────┬───────────┘      │
│                                          │                  │
│                                          ▼                  │
│  ENVIRONMENT ZONES           ┌───────────────────────┐      │
│  ┌──────────────────┐        │ DAMAGE HANDLER        │      │
│  │ "Freezing Area"  │───────▶│ Apply DOT (If < 0)    │      │
│  └──────────────────┘        └───────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Use a Global Tick (e.g., every 1s) instead of `Update()` for stats.
- ✅ Define stats as ScriptableObjects if the list is dynamic.
- ✅ Use generic "Effect" classes for Buffs/Debuffs.
- ✅ Visualize hazards clearly (Post-processing, UI icons).
- ❌ **NEVER** calculate stat decay every frame.
- ❌ **NEVER** hardcode decay rates; use curves or config files.

## Few-Shot Examples

### Example 1: Basic Hunger
**User**: "Add hunger system."

**Agent**:
```csharp
public void OnTick()
{
    // Simple decay
    currentHunger = Mathf.Max(0, currentHunger - decayRate);
    
    if (currentHunger <= 0)
    {
        healthSystem.TakeDamage(10);
    }
}
```

### Example 2: Temperature Zone
**User**: "Create a freezing zone."

**Agent**:
```csharp
public class TemperatureZone : MonoBehaviour
{
    [SerializeField] private float _targetTemp = -10f;
    
    private void OnTriggerStay(Collider other)
    {
        if (other.TryGetComponent(out TemperatureSystem temp))
        {
            temp.SetExternalTemp(_targetTemp);
        }
    }
}
```

## Related Skills
- `@unity-events-messaging` - Notify UI of changes
- `@player-movement-controller` - Reduce speed when starving
