---
name: coreclr-gc-watchdog
description: "Detects, diagnoses, and eliminates Garbage Collector pressure in Unity (CoreCLR). Provides patterns for zero-alloc code, Profiler integration guidance, and a GC budget monitoring protocol."
version: 2.0.0
tags: ["performance", "gc", "memory", "coreclr", "allocation", "profiling", "optimization"]
argument-hint: "action='audit' OR action='fix' target='Assets/Scripts/MySystem.cs'"
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
  gc_alloc_per_frame: "0 bytes (target)"
  max_update_cost: "Profiler-verified per system"
tdd_first: false
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - read_resource
---

# CoreCLR GC Watchdog

## Overview
Unity 6 runs on **CoreCLR**, a modern .NET runtime with a generational garbage collector. While CoreCLR is more efficient than Mono, uncontrolled GC allocations still cause **frame spikes** (GC.Collect pauses). This skill audits code for allocation hot-spots, classifies the allocation sources, and applies zero-alloc patterns to eliminate the pressure.

## When to Use
- Use when the Unity Profiler's **GC Alloc** column shows non-zero values in `Update()` loops.
- Use when the **Memory Profiler** reveals growing heap fragmentation over time.
- Use during a **Performance Audit** (e.g., before a mobile release).
- ❌ Do NOT use for one-time allocations in `Awake()` or `Start()` — those are fine.

## GC Pressure Classification

| Allocation Source | Severity | Zero-Alloc Replacement |
|-------------------|----------|------------------------|
| `new List<T>()` in `Update()` | 🔴 Critical | Pre-allocate + `.Clear()` |
| LINQ (`.Where()`, `.Select()`) in hot path | 🔴 Critical | `for` loop |
| `string +` concatenation in loop | 🔴 Critical | `StringBuilder` |
| `GetComponent<T>()` in `Update()` | 🟠 High | Cache in `Awake()` |
| Boxing value types (`int` as `object`) | 🟠 High | Generic methods / `IEquatable<T>` |
| Delegates / lambdas (allocation on capture) | 🟡 Medium | Cache delegate as field |
| `params object[]` variadic args | 🟡 Medium | Overloads or `Span<T>` |
| `foreach` on non-generic `IEnumerable` | 🟢 Low | Use generic `IEnumerable<T>` |

## Profiler Integration Workflow

```
1. Open Window → Analysis → Profiler
2. Record a gameplay session (10-30 seconds)
3. Click "GC Alloc" column to sort by allocation size
4. Identify the largest allocating frame
5. Drill into the call stack → find the responsible method
6. Apply the fix pattern from the Classification table above
7. Re-record → verify column shows 0B
```

### Key Profiler Markers to Watch
- `GC.Alloc` — direct allocation spike
- `GC.Collect` — mark-and-sweep pause (stop-the-world)
- `UnsafeUtility.Malloc` — NativeArray allocation (acceptable if persistent)

## Procedure

1.  **Profile First**: Never optimize by guessing. Use the Profiler to pinpoint the hot frame.
2.  **Identify Source**: Read the call stack for the GC.Alloc marker.
3.  **Classify**: Match to the GC Pressure table.
4.  **Apply Pattern**: Use the zero-alloc replacement.
5.  **Re-Validate**: Record again to confirm 0B in that callsite.

## Best Practices

- ✅ Pre-allocate collections in `Awake()` with estimated capacity. Call `.Clear()` instead of `new`.
- ✅ Use `ArrayPool<T>.Shared.Rent()` / `.Return()` for temporary arrays.
- ✅ Use `Span<T>` over stack or pre-allocated memory for intermediate computations.
- ✅ Cache delegates: `private readonly Action _onUpdate = OnUpdate;` in the field.
- ✅ Use `StringBuilder` for runtime string composition; use `string.Format` sparingly.
- ❌ **NEVER** allocate inside `Update()`, `FixedUpdate()`, or `OnTriggerStay()`.
- ❌ **NEVER** use LINQ in a hot path — every `.Where().ToList()` is a new allocation.
- ❌ **NEVER** pass a value-type struct to a method expecting `object` (boxing).

## Few-Shot Examples

### Example 1: Pre-allocating a List
```csharp
// ❌ BEFORE — allocates every frame
private void Update()
{
    var enemies = new List<Enemy>(); // GC ALLOC!
    FindEnemiesInRange(enemies);
}

// ✅ AFTER — zero alloc
private readonly List<Enemy> _enemyBuffer = new(32);

private void Update()
{
    _enemyBuffer.Clear(); // reuse, no alloc
    FindEnemiesInRange(_enemyBuffer);
}
```

### Example 2: Caching a Delegate
```csharp
// ❌ BEFORE — lambda captured as new alloc every call
private void SubscribeEvents()
{
    _button.onClick.AddListener(() => OnButtonClicked()); // alloc!
}

// ✅ AFTER — cache the delegate
private readonly UnityAction _onButtonClicked;

private void Awake() => _onButtonClicked = OnButtonClicked;
private void OnEnable()  => _button.onClick.AddListener(_onButtonClicked);
private void OnDisable() => _button.onClick.RemoveListener(_onButtonClicked);
```

### Example 3: Span for Temporary Data
```csharp
// ✅ Stack-allocated buffer — zero heap alloc
private void ProcessHits(int hitCount)
{
    Span<RaycastHit> hits = stackalloc RaycastHit[hitCount];
    Physics.RaycastNonAlloc(transform.position, Vector3.forward, /* ... */);
    // Process hits without any heap allocation
}
```

## Related Skills

- `@job-system-burst` — Moves computation off the managed heap entirely
- `@object-pooling-system` — Pre-allocates GameObjects to avoid Instantiate/Destroy GC
- `@memory-profiler-expert` — Deep memory snapshot analysis
