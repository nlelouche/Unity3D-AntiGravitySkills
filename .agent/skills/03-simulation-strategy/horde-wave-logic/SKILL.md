---
name: horde-wave-logic
description: "Wave spawning system for Tower Defense and Survival games. Configurable waves, enemy types, intervals, and difficulty scaling."
version: 2.0.0
tags: ["spawner", "horde", "waves", "enemies", "tower-defense"]
argument-hint: "action='StartWave' config='Wave1' OR spawn='Zombie_Fast'"
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

# Horde & Wave Logic

## Overview
Manages the pacing and spawning of enemy units. Uses ScriptableObjects to define wave configurations, allowing designers to tweak difficulty without touching code.

## When to Use
- Use for Tower Defense games
- Use for "Horde Mode" survival
- Use for timed enemy assaults
- Use for testing combat balance
- Use for creating "Boss Waves"

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WAVE CONTROLLER                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WAVE CONFIG (Asset)      SPAWNER (MonoBehaviour)           │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ Wave 1:        │      │ State: Waiting/Spawning   │      │
│  │ - 10 Zombies   │─────▶│ Timer: 30s                │      │
│  │ - Rate: 0.5s   │      │ Coroutine: SpawnLoop()    │      │
│  └────────────────┘      └─────────────┬─────────────┘      │
│                                        │                    │
│                                        ▼                    │
│    OBJECT POOL            ┌───────────────────────────┐     │
│  ┌────────────────┐       │ Instantiate / GetFromPool │     │
│  │ Zombie Prefab  │◀──────│ Set Position (SpawnPoint) │     │
│  └────────────────┘       └───────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Use **Object Pooling** for enemies (Critical for performance).
- ✅ Define Waves as `ScriptableObjects` (List of Waves).
- ✅ Include "Warmup" time between waves.
- ✅ Support multiple Spawn Points.
- ✅ Implement "Wave Cleared" logic (Track active enemy count).
- ❌ **NEVER** Instantiate enemies during the loop without pooling.
- ❌ **NEVER** use `InvokeRepeating` (hard to control); use Coroutines.

## Few-Shot Examples

### Example 1: Wave Config Data
**User**: "Create data for a wave."

**Agent**:
```csharp
[CreateAssetMenu]
public class WaveData : ScriptableObject
{
    public GameObject EnemyPrefab;
    public int Count;
    public float SpawnRate;
}
```

### Example 2: Spawner Logic
**User**: "Spawn the wave."

**Agent**:
```csharp
IEnumerator SpawnWave(WaveData wave)
{
    for (int i = 0; i < wave.Count; i++)
    {
        SpawnEnemy(wave.EnemyPrefab);
        yield return new WaitForSeconds(wave.SpawnRate);
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
public void HordeWaveLogic_Should{ExpectedBehavior}_When{Condition}()
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
public void HordeWaveLogic_ShouldHandle{EdgeCase}()
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
public void HordeWaveLogic_ShouldThrow_When{InvalidInput}()
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
- `@object-pooling-system` - Required for spawner
- `@unit-population-ai` - AI for spawned units
- `@unity-events-messaging` - "Wave Start/End" events
