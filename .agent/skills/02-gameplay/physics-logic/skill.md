---
name: physics-logic
description: "Unity physics systems: Rigidbody, collisions, triggers, layers, and physics queries (Raycast, OverlapSphere)."
version: 1.0.0
tags: ["gameplay", "physics", "collisions", "rigidbody", "raycast"]
argument-hint: "action='raycast' layer='Enemy' distance='10'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
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

## Related Skills
- `@damage-health-framework` - Damage on collision
- `@advanced-character-controller` - Character physics
- `@navmesh-pathfinding` - AI movement

## Template Files
Available in templates/ folder.
