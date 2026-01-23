---
name: advanced-design-patterns
description: "Principal Architect for SOLID & GoF Patterns in Unity 3D. Activate for complex systems, scalable mechanics, decoupled architectures, or refactoring God Classes."
version: 1.0.0
tags: ["architecture", "patterns", "SOLID", "GoF", "strategy", "factory", "observer", "command"]
argument-hint: "pattern='strategy' name='EnemyBehavior' namespace='Game.AI'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Advanced Design Patterns

## Overview
Transform high-level gameplay requirements into modular, testable, and maintainable systems. This skill enforces strict structural patterns (Strategy, Factory, Observer, Command) adapted for Unity's unique lifecycle.

## When to Use
- Use when implementing any of the GoF design patterns
- Use when refactoring "God Classes" or circular dependencies
- Use when creating interchangeable behaviors (Strategy)
- Use when spawning objects with pooling (Factory)
- Use when implementing decoupled event systems (Observer)
- Use when building undo/redo or input replay systems (Command)

## Available Patterns

| Pattern | Use Case | Template |
|---------|----------|----------|
| **Strategy** | Interchangeable behaviors (AI, attacks) | `IStrategy.cs`, `StrategyContext.cs` |
| **Factory** | Object creation with pooling | `IFactory.cs`, `PooledFactory.cs` |
| **Observer** | Decoupled event notifications | `IObserver.cs` |
| **Command** | Undo/redo, input recording | `ICommand.cs`, `CommandInvoker.cs` |

## Thinking Process (Mandatory)
Before generating code, analyze:
1. **Identify the Axis of Change**: What varies? (Behavior, Creation, Notification)
2. **Pattern Selection**: Justify choice based on problem domain
3. **Unity Compatibility**: MonoBehaviour vs ScriptableObject vs plain C#
4. **SOLID Validation**: SRP and OCP compliance check

## Procedure
1. **Generate Architecture Plan**: Emit class diagram before implementation
2. **Define Contracts**: Create interfaces with clear API boundaries
3. **Implement Concretes**: Build decoupled implementations
4. **Inject Dependencies**: Use VContainer or SO-based injection (no static Singletons!)
5. **Audit**: Verify against constraints

## Best Practices
- ✅ Use interfaces as reference types, not concrete classes
- ✅ Prefer composition over inheritance
- ✅ Every Factory for high-frequency objects MUST use Object Pooling
- ✅ Unsubscribe from events in `OnDisable`/`OnDestroy`
- ✅ Use `[SerializeField] private` with `_camelCase` naming
- ❌ **NEVER** use `GameObject.Find`, `SendMessage`, `BroadcastMessage`
- ❌ **NEVER** use large switch/if-else for behavior selection
- ❌ **NEVER** cast interface back to concrete class

## Architecture Audit Checklist
- [ ] **SRP Compliance**: Each class has single responsibility
- [ ] **Memory Safety**: Events unsubscribed in OnDestroy
- [ ] **Performance**: No heap allocations in Update loops

## Few-Shot Examples

### Example 1: Strategy Pattern for AI
**User**: "I need different enemy AI behaviors like patrolling, chasing, and retreating."

**Agent Output**:
```
1. Generate Implementation Plan with Strategy Pattern
2. Create IEntityBehavior interface
3. Implement PatrolBehavior, ChaseBehavior, RetreatBehavior
4. Create EnemyController with SetBehavior(IBehavior) method
5. Inject behaviors via ScriptableObject references
```

### Example 2: Factory with Pooling
**User**: "Create a projectile spawning system that doesn't cause GC spikes."

**Agent Output**:
```
1. Create IProjectileFactory interface
2. Implement ProjectilePooledFactory : PooledFactory<Projectile>
3. Configure initial pool size based on expected max concurrent
4. Add Return() method call on projectile destruction
```

### Example 3: Observer for UI Updates
**User**: "Update the health bar when player takes damage without coupling."

**Agent Output**:
```
1. Create IHealthObserver interface
2. Create PlayerHealth : ISubject<HealthData>
3. Create HealthBarUI : IObserver<HealthData>
4. Subscribe in OnEnable, unsubscribe in OnDisable
```

## Related Skills
- `@event-bus-system` - For global decoupled events
- `@di-container-manager` - For dependency injection setup
- `@scriptableobject-architecture` - For data-driven pattern implementations

## Generator Script
```bash
python scripts/pattern_gen.py --pattern strategy --name EnemyAI --namespace Game.AI
python scripts/pattern_gen.py --pattern factory --name Projectile --namespace Game.Combat
```