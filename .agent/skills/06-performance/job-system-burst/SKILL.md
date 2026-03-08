---
name: job-system-burst
description: "Implements high-performance parallel CPU workloads using the Unity Job System and Burst Compiler. Achieves near-native C code performance with zero managed allocations."
version: 2.0.0
tags: ["performance", "jobs", "burst", "multithreading", "DOTS", "native", "optimization"]
argument-hint: "job_type='IJob|IJobParallelFor|IJobChunk' name='PathfindingJob'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.unity.burst"
    - "com.unity.collections"
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for:
    - "com.unity.burst"
    - "com.unity.collections"
performance_budget:
  gc_alloc_per_frame: "0 bytes"
  max_update_cost: "O(n/thread_count)"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Job System + Burst

## Overview
The Unity Job System combined with the Burst Compiler enables **deterministic, multi-threaded, allocation-free** CPU computation. Burst compiles C# to highly optimized native machine code (SIMD vectorization, loop unrolling) while the Job System's safety system prevents race conditions at compile time. Use this for any CPU-bound computation: pathfinding, physics simulation, procedural generation, AI decisions.

## When to Use
- Use for operations over large arrays (particles, agents, tiles) that run every frame.
- Use when the Unity Profiler shows a long `Update()` or coroutine blocking the main thread.
- Use for spatial queries, raycasting sweeps, or custom physics integration.
- Use when targeting mobile: single-core optimization is often not enough.
- ❌ Do NOT use for small collections (<100 elements) — scheduling overhead outweighs gains.
- ❌ Do NOT use when accessing `MonoBehaviour` or Unity API during job execution.

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                  JOB SYSTEM PIPELINE                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  MAIN THREAD                 WORKER THREADS               │
│  ┌─────────────┐             ┌────────────────────────┐   │
│  │ Allocate    │             │  Job.Execute(index)    │   │
│  │ NativeArray │────Schedule─▶  (Full Burst Native)  │   │
│  │ (Persistent │             │  NativeArray reads +  │   │
│  │  or TempJob)│             │  writes ONLY          │   │
│  └─────────────┘             └────────────────────────┘   │
│        │                              │                    │
│        │     JobHandle                │                    │
│        └──────────────────────────────┘                   │
│        ▼                                                   │
│  Complete() → Read results on main thread                  │
│                                                            │
│  ALLOCATOR LIFETIMES:                                      │
│  TempJob  → within same frame   (Schedule + Complete)      │
│  Temp     → within same method  (rarely used in jobs)      │
│  Persistent → across frames     (Dispose in OnDestroy)     │
└────────────────────────────────────────────────────────────┘
```

## Job Types

| Type | Use Case | Parallelism |
|------|---------|------------|
| `IJob` | Single task (e.g., pathfinding for one unit) | None |
| `IJobParallelFor` | Same work over N items (e.g., update N agents) | Automatic batch split |
| `IJobFor` | Like ParallelFor but with explicit inner loop control | Manual |
| `IJobChunk` | ECS-only: process entity archetype chunks | Per-chunk |

## TDD Contract

```csharp
// Write these tests BEFORE implementing:
[Test]
public void MovementJob_WhenScheduled_MovesAllAgentsForward()
{
    // Arrange
    var positions = new NativeArray<float3>(10, Allocator.TempJob);
    var velocities = new NativeArray<float3>(10, Allocator.TempJob);
    for (int i = 0; i < 10; i++) velocities[i] = new float3(0, 0, 1);

    // Act
    var job = new MoveAgentsJob { Positions = positions, Velocities = velocities, DeltaTime = 0.016f };
    job.Schedule(10, 64).Complete();

    // Assert
    Assert.AreApproximatelyEqual(0.016f, positions[0].z, 0.001f);

    // Cleanup
    positions.Dispose();
    velocities.Dispose();
}
```

## Procedure

1.  **Context Check**: Verify `com.unity.burst` and `com.unity.collections` are in `manifest.json`.
2.  **Define Job Struct**: Create `[BurstCompile] struct MyJob : IJobParallelFor`.
3.  **Declare NativeArrays**: All data passed via `NativeArray<T>` or `NativeList<T>`.
4.  **Annotate Access**: Use `[ReadOnly]` on input arrays for maximum parallelism.
5.  **Schedule**: Call `job.Schedule(count, batchSize)` → get `JobHandle`.
6.  **Complete**: Call `handle.Complete()` before reading results on main thread.
7.  **Dispose**: Always dispose `NativeArray` in `OnDestroy()` or after use.

## Best Practices

- ✅ Always add `[BurstCompile]` — without it you lose 90% of the gain.
- ✅ Mark read-only inputs with `[ReadOnly]` — enables parallel reads without locking.
- ✅ Use `Allocator.TempJob` for single-frame jobs, `Allocator.Persistent` for multi-frame.
- ✅ Batch schedule multiple jobs using `JobHandle.CombineDependencies()`.
- ✅ Use `Burst Inspector` (Jobs → Burst Inspector) to verify SIMD vectorization.
- ❌ **NEVER** reference `MonoBehaviour`, `GameObject`, or any managed type inside a job.
- ❌ **NEVER** forget to call `.Dispose()` — NativeArrays are unmanaged memory.
- ❌ **NEVER** call `Complete()` immediately after `Schedule()` on the same frame — defeats threading.

## Few-Shot Examples

### Example 1: Parallel Agent Movement (IJobParallelFor)
**User**: "My 500 agents update their positions on the main thread and it's tanking FPS."

**Agent**:
```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using Unity.Mathematics;
using UnityEngine;

[BurstCompile]
public struct MoveAgentsJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float3> Velocities;
    public NativeArray<float3> Positions;
    public float DeltaTime;

    public void Execute(int index)
    {
        Positions[index] += Velocities[index] * DeltaTime;
    }
}

public class AgentSystem : MonoBehaviour
{
    private NativeArray<float3> _positions;
    private NativeArray<float3> _velocities;
    private JobHandle _jobHandle;
    private const int AgentCount = 500;

    private void Awake()
    {
        _positions  = new NativeArray<float3>(AgentCount, Allocator.Persistent);
        _velocities = new NativeArray<float3>(AgentCount, Allocator.Persistent);
    }

    private void Update()
    {
        var job = new MoveAgentsJob
        {
            Positions  = _positions,
            Velocities = _velocities,
            DeltaTime  = Time.deltaTime
        };
        // Schedule: 500 items, 64 per batch
        _jobHandle = job.Schedule(AgentCount, 64);
    }

    private void LateUpdate()
    {
        _jobHandle.Complete(); // Read results after all jobs finish
        // Apply to transforms here...
    }

    private void OnDestroy()
    {
        _jobHandle.Complete(); // Safety: complete before dispose
        _positions.Dispose();
        _velocities.Dispose();
    }
}
```

### Example 2: Single Background Task (IJob)
**User**: "Run a pathfinding calculation on a background thread."

**Agent**:
```csharp
[BurstCompile]
public struct PathfindingJob : IJob
{
    [ReadOnly] public NativeArray<int> Grid;
    public NativeArray<int> ResultPath;
    public int2 Start;
    public int2 End;
    public int GridWidth;

    public void Execute()
    {
        // A* or Djikstra implementation here
        // Pure data — no Unity API calls allowed
    }
}
```

## Performance Notes

| Scenario | Single-threaded | Job System + Burst |
|----------|:--------------:|:-----------------:|
| 500 agent positions | ~8ms | ~0.4ms |
| GC Allocation | Yes (closures) | 0 bytes |
| SIMD vectorization | ❌ | ✅ Auto |

## Related Skills

- `@object-pooling-system` — Pool job result arrays to avoid re-allocation
- `@dots-system-architect` — Jobs are the foundation of ECS/DOTS
- `@memory-profiler-expert` — Validate NativeArray usage patterns
- `@context-discovery-agent` — Verifies Burst is installed

## Template Files

- `templates/JobParallelForTemplate.cs.txt` — IJobParallelFor boilerplate
- `templates/JobSingleTemplate.cs.txt` — IJob boilerplate
- `templates/NativeContainerLifecycle.cs.txt` — Proper Allocate/Dispose pattern
