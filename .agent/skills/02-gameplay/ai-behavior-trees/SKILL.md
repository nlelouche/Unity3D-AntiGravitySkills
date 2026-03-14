---
name: ai-behavior-trees
description: "Implements modular Behavior Trees for AI decision making with composite, decorator, and action nodes."
version: 2.0.0
tags: ["gameplay", "AI", "behavior-tree", "NPCs", "enemies"]
argument-hint: "root='Selector' children='PatrolSequence,ChaseSequence'"
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

# AI Behavior Trees

## Overview
Modular Behavior Tree system for AI decision making. Supports composite nodes (Selector, Sequence), decorators (Inverter, Repeater), and custom action/condition nodes.

## When to Use
- Use when implementing complex enemy AI
- Use when NPCs need decision-making logic
- Use when AI needs to prioritize tasks
- Use when state machines become too complex
- Use when AI behavior needs to be modular/reusable

## Architecture

```
                    ┌─────────────────┐
                    │   Root Selector │
                    └────────┬────────┘
            ┌────────────────┼────────────────┐
            ↓                                 ↓
    ┌───────────────┐               ┌───────────────┐
    │ Chase Sequence│               │ Patrol Sequence│
    └───────┬───────┘               └───────┬───────┘
        ┌───┴───┐                       ┌───┴───┐
        ↓       ↓                       ↓       ↓
    ┌──────┐ ┌──────┐              ┌──────┐ ┌──────┐
    │CanSee│ │MoveTo│              │HasPath│ │Follow │
    │Player│ │Player│              │      │ │Path   │
    └──────┘ └──────┘              └──────┘ └──────┘
```

## Node Types

| Type | Behavior |
|------|----------|
| **Selector** | Tries children until one succeeds (OR) |
| **Sequence** | Runs children until one fails (AND) |
| **Inverter** | Flips child result |
| **Repeater** | Repeats child N times |
| **Condition** | Returns success/failure based on check |
| **Action** | Performs game action |

## Node Return Values
- **Success**: Node completed successfully
- **Failure**: Node failed
- **Running**: Node still processing

## Best Practices
- ✅ Keep nodes small and focused
- ✅ Use Blackboard for shared data
- ✅ Cache frequently used references
- ✅ Use decorators for flow control
- ❌ **NEVER** put heavy calculations in Tick
- ❌ **NEVER** use deep nested trees (max 5-6 levels)

## Few-Shot Examples

### Example 1: Enemy AI
**User**: "Enemy patrols, chases player when seen."

**Agent**:
```
Root Selector
├── Chase Sequence
│   ├── Condition: CanSeePlayer
│   └── Action: MoveToPlayer
└── Patrol Sequence
    ├── Condition: HasPatrolPath
    └── Action: FollowPatrolPath
```

### Example 2: Attack Priority
**User**: "Attack melee if close, else ranged."

**Agent**:
```
Root Selector
├── Melee Sequence
│   ├── Condition: InMeleeRange
│   └── Action: MeleeAttack
└── Ranged Sequence
    ├── Condition: HasAmmo
    └── Action: RangedAttack
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void AiBehaviorTrees_Should{ExpectedBehavior}_When{Condition}()
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
public void AiBehaviorTrees_ShouldHandle{EdgeCase}()
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
public void AiBehaviorTrees_ShouldThrow_When{InvalidInput}()
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
- `@state-machine-architect` - Simpler state-based AI
- `@navmesh-pathfinding` - Movement for AI
- `@damage-health-framework` - Combat integration

## Template Files
Available in templates/ folder.
