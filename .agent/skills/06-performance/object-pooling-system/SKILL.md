---
name: object-pooling-system
description: "High-performance object pooling for GameObjects to eliminate GC spikes and allocation overhead."
version: 2.0.0
tags: ["performance", "pooling", "memory", "GC", "optimization"]
argument-hint: "prefab='Bullet' initial_size='20' OR pool_type='generic'"
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
  check_render_pipeline: true
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes (target)"
  max_update_cost: "Profiler-verified"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
---

# Object Pooling System

## Overview
High-performance object pooling to eliminate GC spikes from Instantiate/Destroy. Essential for projectiles, particles, enemies, and any frequently spawned objects.

## When to Use
- Use for bullets, projectiles, VFX
- Use for spawned enemies, pickups
- Use for UI list items
- Use when experiencing GC spikes
- Use for mobile/console optimization

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   POOLING ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  POOL MANAGER              OBJECT POOLS                     │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │ GetPool<T>() │────────▶│ Pool<Bullet> │                 │
│  │ RegisterPool │         │  ├─ Active[] │                 │
│  │ ReturnAll()  │         │  └─ Available│                 │
│  └──────────────┘         │     Queue<>  │                 │
│                           ├──────────────┤                 │
│  POOLABLE OBJECT          │ Pool<Enemy>  │                 │
│  ┌──────────────┐         └──────────────┘                 │
│  │ IPoolable    │                                          │
│  │  OnSpawn()   │◀────────── Get()                        │
│  │  OnDespawn() │──────────▶ Return()                     │
│  └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Pool Types

| Type | Use Case |
|------|----------|
| **Simple Pool** | Single prefab, fixed size |
| **Generic Pool** | Type-safe, any MonoBehaviour |
| **Expandable** | Grows when exhausted |
| **Multi-Pool** | Multiple prefab variants |

## Performance Impact

| Operation | Without Pool | With Pool |
|-----------|:------------:|:---------:|
| Spawn 100 | ~5ms | ~0.1ms |
| GC Alloc | 100KB+ | 0KB |
| Memory churn | High | None |

## Best Practices
- ✅ Pre-warm pools at scene load
- ✅ Use IPoolable for reset logic
- ✅ Return objects explicitly
- ✅ Set reasonable initial sizes
- ✅ Use component caching
- ❌ **NEVER** Destroy pooled objects
- ❌ **NEVER** forget to return objects
- ❌ **NEVER** use GetComponent on spawn

## Few-Shot Examples

### Example 1: Generic Pool
**User**: "Pool for bullets."

**Agent**:
```csharp
public class ObjectPool<T> where T : MonoBehaviour, IPoolable
{
    private readonly T _prefab;
    private readonly Queue<T> _available = new();
    private readonly List<T> _active = new();
    private readonly Transform _parent;
    
    public ObjectPool(T prefab, int initialSize, Transform parent = null)
    {
        _prefab = prefab;
        _parent = parent;
        
        for (int i = 0; i < initialSize; i++)
        {
            CreateInstance();
        }
    }
    
    public T Get(Vector3 position, Quaternion rotation)
    {
        T obj = _available.Count > 0 ? _available.Dequeue() : CreateInstance();
        obj.transform.SetPositionAndRotation(position, rotation);
        obj.gameObject.SetActive(true);
        obj.OnSpawn();
        _active.Add(obj);
        return obj;
    }
    
    public void Return(T obj)
    {
        obj.OnDespawn();
        obj.gameObject.SetActive(false);
        _active.Remove(obj);
        _available.Enqueue(obj);
    }
}
```

### Example 2: IPoolable Interface
**User**: "Reset logic for pooled object."

**Agent**:
```csharp
public interface IPoolable
{
    void OnSpawn();
    void OnDespawn();
}

public class Bullet : MonoBehaviour, IPoolable
{
    private Rigidbody _rb;
    private TrailRenderer _trail;
    
    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _trail = GetComponent<TrailRenderer>();
    }
    
    public void OnSpawn()
    {
        _rb.velocity = Vector3.zero;
        _trail.Clear();
    }
    
    public void OnDespawn()
    {
        _rb.velocity = Vector3.zero;
    }
}
```

### Example 3: Pool Manager Singleton
**User**: "Centralized pool management."

**Agent**:
```csharp
public class PoolManager : MonoBehaviour
{
    private static PoolManager _instance;
    private readonly Dictionary<Type, object> _pools = new();
    
    public static ObjectPool<T> GetPool<T>() where T : MonoBehaviour, IPoolable
    {
        return (ObjectPool<T>)_instance._pools[typeof(T)];
    }
    
    public void RegisterPool<T>(T prefab, int size) where T : MonoBehaviour, IPoolable
    {
        var pool = new ObjectPool<T>(prefab, size, transform);
        _pools[typeof(T)] = pool;
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
public void ObjectPoolingSystem_Should{ExpectedBehavior}_When{Condition}()
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
public void ObjectPoolingSystem_ShouldHandle{EdgeCase}()
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
public void ObjectPoolingSystem_ShouldThrow_When{InvalidInput}()
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
- `@addressables-asset-management` - Async prefab loading
- `@memory-profiler-expert` - Verify pool effectiveness
- `@mobile-optimization` - Mobile-specific pooling
