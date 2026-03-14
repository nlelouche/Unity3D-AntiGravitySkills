---
name: ability-skill-system
description: "Data-driven ability system with ScriptableObject definitions, cooldowns, resource costs, targeting, and cast times."
version: 2.0.0
tags: ["gameplay", "abilities", "skills", "cooldowns", "RPG", "action"]
argument-hint: "ability_name='Fireball' cooldown='5' cost='Mana:30'"
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

# Ability Skill System

## Overview
Complete data-driven ability system using ScriptableObjects. Supports cooldowns, multiple resource types, targeting modes, cast times, and VFX/SFX integration.

## When to Use
- Use when implementing RPG-style abilities
- Use when creating action game skills
- Use when abilities need cooldowns
- Use when abilities cost resources (mana, energy, stamina)
- Use when abilities need targeting (self, enemy, ground, direction)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AbilityDataSO                            │
│              (ScriptableObject Asset)                       │
├─────────────────────────────────────────────────────────────┤
│  Identity: ID, Name, Description, Icon                      │
│  Cooldown: Duration, Shared Group                           │
│  Costs: [{Type: Mana, Amount: 30}, ...]                     │
│  Targeting: Self, Enemy, AOE, Direction                     │
│  Execution: CastTime, Duration, CanCancel                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AbilityManager                           │
│              (On Player/NPC)                                │
├─────────────────────────────────────────────────────────────┤
│  TryUseAbility(slotIndex, context)                          │
│  Cooldown Tracking, Resource Management                     │
│  Events: OnCooldownStarted, OnResourceChanged               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AbilityExecutor                          │
│              (Handles Cast + Effect)                        │
├─────────────────────────────────────────────────────────────┤
│  StartCast(context), Execute(context)                       │
│  Spawn VFX, Play SFX, Apply Effects                         │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| `AbilityDataSO` | ScriptableObject with ability definition |
| `AbilityManager` | Main controller with cooldowns/resources |
| `AbilityExecutor` | Handles casting and effect execution |
| `AbilitySlot` | Binds ability to hotkey |
| `IResourceProvider` | Interface for resource systems |

## Resource Types
- **Mana**: Standard caster resource
- **Energy**: Regenerates quickly
- **Stamina**: Physical abilities
- **Rage**: Builds in combat
- **Combo**: Chain attacks
- **Ammo**: Consumable projectiles

## Best Practices
- ✅ Use ScriptableObjects for ability data (designer-friendly)
- ✅ Separate data (AbilityDataSO) from execution (AbilityExecutor)
- ✅ Use shared cooldown groups for similar abilities
- ✅ Implement IResourceProvider for custom resource systems
- ✅ Subscribe to events for UI updates
- ❌ **NEVER** hardcode ability stats in code
- ❌ **NEVER** mix ability data with character stats

## Few-Shot Examples

### Example 1: Create Fireball Ability
**User**: "Create a fireball ability with 5s cooldown, 30 mana cost."

**Agent**:
```csharp
// 1. Create AbilityDataSO asset: Assets/Abilities/Fireball.asset
// 2. Set: CooldownDuration = 5, Costs = [{Mana, 30}]
// 3. Set: TargetType = PointOnGround, Range = 10
// 4. Assign VFX prefab and SFX clip
```

### Example 2: Cooldown UI
**User**: "Show ability cooldown on button."

**Agent**:
```csharp
abilityManager.OnCooldownStarted += (ability, duration) =>
{
    if (ability == myAbility)
        StartCooldownDisplay(duration);
};
```

### Example 3: Resource Cost Check
**User**: "Gray out button if not enough mana."

**Agent**:
```csharp
bool canUse = abilityManager.HasResource(ResourceType.Mana, ability.Costs[0].Amount) 
           && !abilityManager.IsOnCooldown(ability);
button.interactable = canUse;
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void AbilitySkillSystem_Should{ExpectedBehavior}_When{Condition}()
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
public void AbilitySkillSystem_ShouldHandle{EdgeCase}()
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
public void AbilitySkillSystem_ShouldThrow_When{InvalidInput}()
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
- `@damage-health-framework` - Damage dealing abilities
- `@status-effect-system` - Buff/debuff abilities
- `@scriptableobject-architecture` - Data-driven design

## Template Files
- `templates/AbilityDataSO.cs.txt` - ScriptableObject definition
- `templates/AbilityManager.cs.txt` - Main controller
- `templates/AbilityExecutor.cs.txt` - Execution handler
