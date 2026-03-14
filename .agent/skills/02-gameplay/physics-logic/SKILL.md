---
name: physics-logic
description: "Unity physics systems: Rigidbody, collisions, triggers, layers, and physics queries (Raycast, OverlapSphere)."
version: 2.0.0
tags: ["gameplay", "physics", "collisions", "rigidbody", "raycast"]
argument-hint: "action='raycast' layer='Enemy' distance='10'"
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

# Physics Logic

## Overview
Unity physics systems covering Rigidbody dynamics, collision detection, triggers, layer matrices, and physics queries.

## When to Use
- Use when objects need realistic movement
- Use when detecting collisions/triggers
- Use when implementing raycast weapons
- Use when checking line of sight
- Use when implementing physics-based abilities

## Physics Queries

| Query | Use Case |
|-------|----------|
| `Physics.Raycast` | Line of sight, hitscan weapons |
| `Physics.SphereCast` | Projectile with radius |
| `Physics.OverlapSphere` | AOE detection |
| `Physics.BoxCast` | Melee swing detection |
| `Physics.CapsuleCast` | Character movement checks |

## Collision vs Trigger
```
┌─────────────────────────────────────────────────────────────┐
│                    COLLISION                                │
│  OnCollisionEnter/Stay/Exit                                 │
│  • Both have Colliders                                      │
│  • At least one has Rigidbody                               │
│  • Neither is Trigger                                       │
│  • Physical response (push, bounce)                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    TRIGGER                                  │
│  OnTriggerEnter/Stay/Exit                                   │
│  • One has "Is Trigger" enabled                             │
│  • At least one has Rigidbody                               │
│  • No physical response                                     │
│  • Used for detection zones                                 │
└─────────────────────────────────────────────────────────────┘
```

## Layer Best Practices
- ✅ Use layers to filter collisions
- ✅ Configure Layer Collision Matrix
- ✅ Use LayerMask for queries
- ✅ Cache LayerMask values
- ❌ **NEVER** use string layer names at runtime
- ❌ **NEVER** raycast on "Everything" layer

## Few-Shot Examples

### Example 1: Raycast Weapon
**User**: "Shoot raycast and deal damage."

**Agent**:
```csharp
LayerMask enemyLayer = LayerMask.GetMask("Enemy");

if (Physics.Raycast(origin, direction, out RaycastHit hit, 100f, enemyLayer))
{
    if (hit.collider.TryGetComponent<IDamageable>(out var target))
        target.TakeDamage(new DamageInfo(25f));
}
```

### Example 2: AOE Detection
**User**: "Find all enemies in 5m radius."

**Agent**:
```csharp
Collider[] hits = Physics.OverlapSphere(center, 5f, enemyLayer);
foreach (var hit in hits)
{
    // Process each enemy
}
```

### Example 3: Ground Check
**User**: "Check if character is grounded."

**Agent**:
```csharp
bool isGrounded = Physics.SphereCast(
    transform.position + Vector3.up,
    0.3f,
    Vector3.down,
    out _,
    1.1f,
    groundLayer
);
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void PhysicsLogic_Should{ExpectedBehavior}_When{Condition}()
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
public void PhysicsLogic_ShouldHandle{EdgeCase}()
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
public void PhysicsLogic_ShouldThrow_When{InvalidInput}()
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
- `@damage-health-framework` - Damage on collision
- `@advanced-character-controller` - Character physics
- `@navmesh-pathfinding` - AI movement

## Template Files
Available in templates/ folder.

## Best Practices
- Follow the patterns and constraints documented in this skill.
- Always run @context-discovery-agent before applying this skill to verify environment compatibility.
- Apply TDD where applicable: write the interface contract first, then implement.
- Zero GC in hot paths: cache references, avoid LINQ and 
ew allocations in Update loops.