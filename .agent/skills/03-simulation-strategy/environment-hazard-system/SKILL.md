---
name: environment-hazard-system
description: "Implementation of survival mechanics including hunger, thirst, temperature, and atmospheric hazards."
version: 2.0.0
tags: ["survival", "hazards", "environment", "status-effects", "gameplay"]
argument-hint: "feature='Hunger' params='decay_rate=1' OR hazard='radiation_zone'"
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



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void EnvironmentHazardSystem_Should{ExpectedBehavior}_When{Condition}()
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
public void EnvironmentHazardSystem_ShouldHandle{EdgeCase}()
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
public void EnvironmentHazardSystem_ShouldThrow_When{InvalidInput}()
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
- `@unity-events-messaging` - Notify UI of changes
- `@player-movement-controller` - Reduce speed when starving
