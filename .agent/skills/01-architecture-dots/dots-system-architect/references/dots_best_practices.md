# DOTS & ECS Best Practices Refresher (2025/2026 Edition)

## 1. Data Design & Memory Layout
- **Archetypes matter**: Adding/Removing components changes the archetype and moves the entity in memory (structural change). Minimize these operations in the main loop.
- **Enableable Components**: Use `IEnableableComponent` instead of adding/removing tags if you toggle behavior frequently. It keeps the same archetype but sets a bitmask.
- **Aspects**: Use `IAspect` to group components logic (e.g., `MoveAspect` wraps Transform and Velocity). It simplifies the `OnUpdate` code.

## 2. Iteration Strategy
| Approach | Usage | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **SystemAPI.Query** | Main Thread | Simple, instant access | Single threaded. Bad for 10k+ entities. |
| **IJobEntity** | Parallel Workers | Best balance of ease/perf | Requires understanding `ref`/`in` params. |
| **IJobChunk** | Raw Chunk Access | Absolute max performace | Verbose, manual chunk iteration. Complex. |

**Guideline**: Default to `IJobEntity` (`ScheduleParallel`) for extensive calculations. Use `SystemAPI.Query` only for structural changes or debug interactions.

## 3. Burst Compiler Rules
- **No Managed Objects**: Classes (`string`, `List<T>`, `GameObject`) are illegal inside a Burst job.
- **Exceptions**: `Debug.Log` works but is stripped in builds unless configured. prefer `UnityEngine.Debug`.
- **Mathematics**: Use `Unity.Mathematics` (`float3`, `quaternion`) instead of `UnityEngine.Vector3`. It is SIMD optimized.
  - `float3` is NOT a 1:1 replacement for `Vector3`. `math.lerp` vs `Vector3.Lerp`.

## 4. Safety & Race Conditions
- **RefRW vs RefRO**: Always use `RefRO<T>` if you don't intend to write. This tells the Job Safety System that multiple jobs can read this data in parallel without blocking.
- **Entity Command Buffer (ECB)**: NEVER destroy entities or add components directly inside a parallel job. Record the command in an ECB (`SystemAPI.GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()`) and play it back later.

## 5. Common Pitfalls
- **Boxing**: Creating a struct but passing it as an interface to a non-generic method causes boxing (allocation).
- **Strings**: Use `FixedString32Bytes`, `FixedString64Bytes`, etc. inside components.
