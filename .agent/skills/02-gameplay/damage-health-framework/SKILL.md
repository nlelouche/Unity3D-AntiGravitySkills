---
name: damage-health-framework
description: "Complete damage and health system with IDamageable interface, damage types, resistances, and event-driven architecture."
version: 2.0.0
tags: ["gameplay", "combat", "health", "damage", "IDamageable"]
argument-hint: "action='create_health' OR damage_type='Fire' resistance='0.5'"
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

# Damage Health Framework

## Overview
Complete damage and health system with interface-driven design, multiple damage types, resistance calculations, and event-driven architecture for UI/VFX integration.

## When to Use
- Use when implementing health for players, enemies, or destructibles
- Use when creating damage types (Physical, Fire, Ice, etc.)
- Use when implementing resistance/vulnerability systems
- Use when building combat systems with critical hits
- Use when UI needs to react to health changes

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      IDamageable                            │
├─────────────────────────────────────────────────────────────┤
│  TakeDamage(DamageInfo) → DamageResult                      │
│  CurrentHealth, MaxHealth, IsAlive                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ↓                  ↓                  ↓
   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
   │   Player      │  │    Enemy      │  │ Destructible  │
   │HealthComponent│  │HealthComponent│  │HealthComponent│
   └───────────────┘  └───────────────┘  └───────────────┘
           ↑
   ┌───────────────┐
   │ DamageDealer  │ ─→ Weapon, Projectile, Hazard
   └───────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| `IDamageable` | Interface for damageable entities |
| `DamageInfo` | Struct with damage details (amount, type, source) |
| `DamageResult` | Struct with damage outcome (dealt, blocked, killed) |
| `HealthComponent` | Reusable MonoBehaviour with events |
| `DamageDealer` | Component for damage sources |

## Damage Types
- **Physical**: Standard melee/ranged damage
- **Fire/Ice/Lightning**: Elemental damage
- **Poison**: Damage over time
- **Holy/Dark**: Magic types
- **True**: Ignores all resistances

## Best Practices
- ✅ Use `DamageInfo` struct for all damage passing
- ✅ Subscribe to events for UI, VFX, audio responses
- ✅ Use resistances for enemy variety
- ✅ Critical hits for exciting combat
- ✅ Implement `IDamageable` on anything destructible
- ❌ **NEVER** modify health directly - use TakeDamage/Heal
- ❌ **NEVER** forget to unsubscribe from events

## Events
```csharp
OnDamaged(DamageResult)   // After damage applied
OnHealed(float amount)     // After healing
OnHealthChanged(current, max)  // Any health change
OnDeath()                  // When health reaches zero
OnRevive()                 // When revived from death
```

## Few-Shot Examples

### Example 1: Basic Enemy Setup
**User**: "Create an enemy with 100 health that takes fire damage."

**Agent**:
```csharp
// Add HealthComponent to enemy
var health = enemy.AddComponent<HealthComponent>();
// Configure in inspector: MaxHealth = 100
// Set Fire resistance to -0.5 (takes 50% extra fire damage)
```

### Example 2: Weapon Damage
**User**: "Make a sword that deals 25 physical damage with 10% crit."

**Agent**:
```csharp
var dealer = sword.AddComponent<DamageDealer>();
dealer.SetDamage(25f);
dealer.SetCritChance(0.1f);
```

### Example 3: Health UI Integration
**User**: "Update health bar when player takes damage."

**Agent**:
```csharp
healthComponent.OnHealthChanged += (current, max) => 
{
    healthBar.value = current / max;
};
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void DamageHealthFramework_Should{ExpectedBehavior}_When{Condition}()
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
public void DamageHealthFramework_ShouldHandle{EdgeCase}()
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
public void DamageHealthFramework_ShouldThrow_When{InvalidInput}()
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
- `@status-effect-system` - Poison, burn, bleed effects
- `@ability-skill-system` - Abilities that deal damage
- `@interface-driven-development` - IDamageable pattern

## Template Files
- `templates/IDamageable.cs.txt` - Core interface + structs
- `templates/HealthComponent.cs.txt` - Reusable health component
- `templates/DamageDealer.cs.txt` - Damage source component
