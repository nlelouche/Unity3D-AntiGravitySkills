---
name: csharp12-features-guide
description: "Practical guide to C#12 and C#13 language features in the Unity 6 / CoreCLR context. Covers primary constructors, collection expressions, ref readonly parameters, and Span<T> idioms."
version: 2.0.0
tags: ["governance", "csharp", "csharp12", "coreclr", "language-features", "performance", "modern"]
argument-hint: "feature='primary-constructors' OR feature='collection-expressions' OR feature='span'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes (feature-dependent — see table)"
  max_update_cost: "Depends on usage pattern"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - read_resource
  - write_to_file
---

# C#12 Features Guide (Unity 6 / CoreCLR)

## Overview
Unity 6 ships with **CoreCLR** and the Roslyn compiler supporting **C#12** (with select C#13 additions). This guide maps each language feature to its **Unity-specific use case**, explains the **GC implications** (critical for game loops), and provides patterns that are safe to use in hot paths vs. initialization-only.

## When to Use
- Use when adopting C# 12/13 features in a Unity 6 project.
- Use to validate whether a feature is safe in hot paths before using it.
- Use during code reviews to justify modern syntax choices.

## Feature Safety Matrix

| Feature | Safe in Update()? | GC Alloc? | Notes |
|---------|:-----------------:|:---------:|-------|
| **Primary Constructors** | N/A (compile-time) | No | Reduces boilerplate |
| **Collection Expressions** `[1,2,3]` | ⚠️ Read note | No* | Use for init only; inline creates array |
| **ref readonly parameters** | ✅ Hot path safe | No | Pass large structs by readonly ref |
| **Span\<T\>** | ✅ Hot path safe | No | Stack-allocated slices |
| **Default lambda params** | Init only | No | `void Foo(int x = 5)` in lambdas |
| **Inline arrays** | ✅ Hot path safe | No | Fixed-size stack buffers |
| **`nameof` operator** | ✅ | No | Always prefer over string literals |

## Feature Deep-Dives

### 1. Primary Constructors
Reduces class boilerplate — ideal for services, models, and ViewModels.

```csharp
// ❌ Old C#10 boilerplate
public class AudioService : IAudioService
{
    private readonly IAudioMixer _mixer;
    public AudioService(IAudioMixer mixer) { _mixer = mixer; }
}

// ✅ C#12 Primary Constructor
public class AudioService(IAudioMixer mixer) : IAudioService
{
    // 'mixer' is a primary parameter — directly accessible in the class body
    public void PlayOneShot(int clipId) => _mixer.Play(clipId);
}
```
**Unity Rule**: Primary constructors work in plain C# classes. MonoBehaviours still use `Awake()` for initialization — do NOT add custom constructors to MonoBehaviours.

---

### 2. Collection Expressions
Concise syntax for initializing arrays, lists, and spans.

```csharp
// ✅ Clean initialization (init time only — safe)
int[] primes = [2, 3, 5, 7, 11, 13];
List<string> tags = ["fire", "explosive", "boss"];

// ✅ Spread operator for merging
int[] combined = [..primes, 17, 19];

// ⚠️ NEVER use inline in Update() — it creates a new array each frame
private void Update()
{
    // ❌ BAD: new array every frame
    foreach (var tag in (string[])["fire", "water"]) { }
}
```

---

### 3. `ref readonly` Parameters
Pass large structs by reference without allowing mutation. Zero GC, zero copy.

```csharp
// Avoids copying a 48-byte struct on every call
public float CalculateDamage(ref readonly DamageContext ctx)
{
    return ctx.BaseDamage * ctx.Multiplier;
}

// Caller
CalculateDamage(ref readonly damageCtx);
```
**Unity hot path use**: Pass `NativeArray<T>` slices, `Vector3` matrices, or custom unmanaged structs.

---

### 4. `Span<T>` and Stack Allocation
The most impactful feature for zero-alloc game loops.

```csharp
// Stack-allocate a buffer of 16 raycast hits — no heap alloc
public void DetectNearbyEnemies()
{
    Span<Collider> results = stackalloc Collider[16];
    int count = Physics.OverlapSphereNonAlloc(
        transform.position, _detectionRadius, _resultBuffer);

    for (int i = 0; i < count; i++)
        ProcessEnemy(results[i]);
}
```
**Limit**: `stackalloc` should be <1KB (typically ≤256 elements). For larger buffers, use `ArrayPool<T>`.

---

### 5. Inline Arrays (C#12)
Declare fixed-size arrays as stack-allocated structs.

```csharp
[System.Runtime.CompilerServices.InlineArray(8)]
public struct WeaponSlots
{
    private IWeapon _element0;
}

// Usage — behaves like a fixed-size array, zero heap alloc
var slots = new WeaponSlots();
slots[0] = new Sword();
```

---

### 6. `nameof` for Property Paths
Always use `nameof` in `INotifyPropertyChanged` and UI Toolkit bindings.

```csharp
// ❌ Magic string — breaks on rename
propertyChanged?.Invoke(this, new("Health"));

// ✅ Refactor-safe
propertyChanged?.Invoke(this, new(nameof(Health)));
```

## Best Practices

- ✅ Use **primary constructors** for services, repositories, and ViewModels.
- ✅ Use **collection expressions** only at initialization time (Awake/Start).
- ✅ Use **ref readonly** for any struct >16 bytes passed frequently.
- ✅ Use **Span\<T\>** for temporary intermediate data instead of arrays.
- ❌ **NEVER** use collection expressions inside `Update()` — they allocate.
- ❌ **NEVER** add constructors to `MonoBehaviour` subclasses.
- ❌ **NEVER** exceed ~1KB with `stackalloc` — stack overflow risk.

## Unity Version Gate

```csharp
// Check before using C#12 features in shared code:
// ProjectSettings/ProjectVersion.txt → m_EditorVersion: 6000.x = Unity 6
// Unity 6 ships with Roslyn C#12 support by default.
// Unity 2022 LTS → C#10 only.
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void Csharp12FeaturesGuide_Should{ExpectedBehavior}_When{Condition}()
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
public void Csharp12FeaturesGuide_ShouldHandle{EdgeCase}()
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
public void Csharp12FeaturesGuide_ShouldThrow_When{InvalidInput}()
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

- `@unified-style-guide` — Enforces naming and formatting for new syntax
- `@coreclr-gc-watchdog` — Validates that new features don't introduce allocations
- `@job-system-burst` — `Span<T>` and `NativeArray<T>` complement each other
