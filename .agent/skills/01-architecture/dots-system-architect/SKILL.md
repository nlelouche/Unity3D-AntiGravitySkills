---
name: dots-system-architect
description: "Unity DOTS architecture specialist for ECS, Jobs, and Burst Compiler performance systems."
version: 2.0.0
tags: ["architecture", "DOTS", "ECS", "Jobs", "Burst", "performance"]
argument-hint: "system_name='MovementSystem' OR component='PlayerData'"
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

# DOTS System Architect

## Overview
Unity Data-Oriented Technology Stack (DOTS) for high-performance game systems. Covers Entity Component System (ECS), C# Job System, and Burst Compiler.

## When to Use
- Use when thousands of entities need processing
- Use when CPU performance is critical
- Use when traditional OOP becomes a bottleneck
- Use when building simulation-heavy games
- Use when maximizing multi-core utilization

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DOTS ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Entities   │    │ Components  │    │  Systems    │     │
│  │  (IDs only) │───▶│  (Data)     │◀───│  (Logic)    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                               │             │
│                                               ▼             │
│                                    ┌─────────────────┐     │
│                                    │   Job System    │     │
│                                    │  (Parallelism)  │     │
│                                    └────────┬────────┘     │
│                                              │              │
│                                              ▼              │
│                                    ┌─────────────────┐     │
│                                    │ Burst Compiler  │     │
│                                    │  (Native Code)  │     │
│                                    └─────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Entity** | Just an ID, no data |
| **Component** | Pure data (struct with IComponentData) |
| **System** | Logic that processes components |
| **Archetype** | Unique component combination |
| **Chunk** | Memory block for same-archetype entities |

## Component Types
- `IComponentData` - Standard component data
- `IBufferElementData` - Dynamic buffer
- `ISharedComponentData` - Shared between entities
- `ICleanupComponentData` - Cleanup on destroy

## Best Practices
- ✅ Keep components small and focused
- ✅ Use Burst for all systems when possible
- ✅ Prefer IJobEntity over manual queries
- ✅ Use EntityCommandBuffer for structural changes
- ✅ Profile with Entity Debugger
- ❌ **NEVER** use managed types in components
- ❌ **NEVER** allocate in Burst-compiled code
- ❌ **NEVER** make structural changes during system update

## Few-Shot Examples

### Example 1: Simple Component
**User**: "Create a health component for ECS."

**Agent**:
```csharp
public struct HealthComponent : IComponentData
{
    public float Current;
    public float Max;
}
```

### Example 2: Movement System
**User**: "Create a system that moves entities."

**Agent**:
```csharp
[BurstCompile]
public partial struct MovementSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float dt = SystemAPI.Time.DeltaTime;
        
        foreach (var (transform, velocity) in 
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
        {
            transform.ValueRW.Position += velocity.ValueRO.Value * dt;
        }
    }
}
```

### Example 3: Spawning Entities
**User**: "Spawn 1000 enemies."

**Agent**:
```csharp
var ecb = new EntityCommandBuffer(Allocator.Temp);
for (int i = 0; i < 1000; i++)
{
    var entity = ecb.CreateEntity();
    ecb.AddComponent(entity, new HealthComponent { Current = 100, Max = 100 });
    ecb.AddComponent(entity, new EnemyTag());
}
ecb.Playback(EntityManager);
ecb.Dispose();
```

## Performance Tips
- **Burst**: 10-100x faster than regular C#
- **Jobs**: Automatic multi-threading
- **Chunks**: Cache-friendly memory layout
- **SOA**: Structure of Arrays vs AOS



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void DotsSystemArchitect_Should{ExpectedBehavior}_When{Condition}()
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
public void DotsSystemArchitect_ShouldHandle{EdgeCase}()
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
public void DotsSystemArchitect_ShouldThrow_When{InvalidInput}()
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
- `@advanced-design-patterns` - Traditional patterns
- `@asynchronous-programming` - Async operations
- `@physics-logic` - Unity Physics (DOTS)

## Required Packages
- `com.unity.entities`
- `com.unity.burst`
- `com.unity.collections`
