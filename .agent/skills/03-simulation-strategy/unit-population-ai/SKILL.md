---
name: unit-population-ai
description: "Optimization-focused AI manager for handling large crowds or populations. Uses time-sliced updates to prevent performance bottlenecks."
version: 2.0.0
tags: ["ai", "population", "crowds", "optimization", "rts"]
argument-hint: "action='Register' count=100 OR type='Worker'"
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

# Unit Population AI

## Overview
Efficiently manages high unit counts (100ts-1000s) by centralized update loops. Instead of every unit running `Update()`, the Manager iterates through them, often time-slicing (updating only X units per frame).

## When to Use
- Use for RTS games with many units
- Use for City Builder attributes (citizens walking)
- Use for Horde games (Zombies)
- Use for Boids/Flocking simulation
- Use for reducing heavy CPU overhead

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    POPULATION MANAGER                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INDIVIDUAL UNIT          CENTRAL MANAGER                   │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ Data (Struct)  │◀─────│ List<Unit> AllUnits       │      │
│  │ - Position     │      │                           │      │
│  │ - State        │      │ Update() {                │      │
│  │ - Target       │      │   // Process 50 per frame │      │
│  └────────────────┘      │   for(i..i+50)            │      │
│                          │     RunLogic(units[i])    │      │
│                          │ }                         │      │
│                          └───────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Use **Structs** or lightweight classes for unit data.
- ✅ Use **Time-Slicing** (Throttle updates).
- ✅ Start Coroutines or Jobs from the Manager, not the Unit.
- ✅ Use Unity **Jobs System** + **Burst** for extreme numbers.
- ❌ **NEVER** put complex logic in `Update()` of a prefab intended to be instantiated 1000 times.
- ❌ **NEVER** use `Find` or `GetComponent` inside the loop.

## Few-Shot Examples

### Example 1: Manager Loop
**User**: "Update 1000 units."

**Agent**:
```csharp
void Update()
{
    // Update 50 units per frame
    int batchSize = 50;
    for (int i = 0; i < batchSize; i++)
    {
        _currentIndex = (_currentIndex + 1) % _units.Count;
        _units[_currentIndex].Tick_LowFrequency();
    }
}
```

### Example 2: Unit Registration
**User**: "Add unit to manager."

**Agent**:
```csharp
public class Unit : MonoBehaviour
{
    void Start() => PopulationManager.Instance.Register(this);
    void OnDestroy() => PopulationManager.Instance.Remove(this);
    
    public void Tick_LowFrequency()
    {
        // Simple AI logic here
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
public void UnitPopulationAi_Should{ExpectedBehavior}_When{Condition}()
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
public void UnitPopulationAi_ShouldHandle{EdgeCase}()
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
public void UnitPopulationAi_ShouldThrow_When{InvalidInput}()
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
- `@object-pooling-system` - Pooling units
- `@mobile-optimization` - CPU budgeting
- `@performance-profiling` - Checking frame times
