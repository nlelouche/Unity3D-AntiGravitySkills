---
name: event-bus-system
description: "Implements a global decoupled Event Bus for cross-system communication. Zero-allocation struct events prevent GC spikes."
version: 1.0.0
tags: ["architecture", "events", "decoupling", "observer", "messaging"]
argument-hint: "event_name='PlayerDamaged' namespace='Game.Events'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Event Bus System

## Overview
Implement global decoupled communication between systems using a static Event Bus. Uses struct-based events to avoid garbage collection allocations during gameplay.

## When to Use
- Use when systems need to communicate without direct references
- Use when implementing publish-subscribe patterns
- Use when reducing dependencies between unrelated systems
- Use when broadcasting global game events (PlayerDied, LevelCompleted)
- Use when UI needs to react to gameplay without coupling

## Architecture

```
┌──────────────┐    Publish(event)    ┌──────────────┐
│   Player     │ ───────────────────→ │   EventBus   │
│  (Publisher) │                      │   (Static)   │
└──────────────┘                      └───────┬──────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              ↓                               ↓                               ↓
      ┌───────────────┐              ┌───────────────┐              ┌───────────────┐
      │   HealthUI    │              │ AchievementSys│              │   Analytics   │
      │  (Subscriber) │              │  (Subscriber) │              │  (Subscriber) │
      └───────────────┘              └───────────────┘              └───────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| `IEvent` | Marker interface for all events |
| `EventBus` | Static class handling subscriptions |
| `GameEvents.cs` | Collection of event struct definitions |
| `EventListenerBase<T>` | Abstract MonoBehaviour for automatic lifecycle |

## Procedure
1. **Define Events**: Create structs implementing `IEvent`
2. **Publish Events**: Call `EventBus.Publish(new YourEvent { ... })`
3. **Subscribe**: Call `EventBus.Subscribe<YourEvent>(HandleEvent)` in `OnEnable`
4. **Unsubscribe**: Call `EventBus.Unsubscribe<YourEvent>(HandleEvent)` in `OnDisable`

## Best Practices
- ✅ Use **structs** for events (zero allocation)
- ✅ Keep events immutable (readonly fields)
- ✅ ALWAYS unsubscribe in `OnDisable` or `OnDestroy`
- ✅ Use `EventListenerBase<T>` for automatic lifecycle
- ✅ Group related events in single file (e.g., `CombatEvents.cs`)
- ❌ **NEVER** forget to unsubscribe (causes memory leaks)
- ❌ **NEVER** use events for high-frequency per-frame logic
- ❌ **NEVER** put heavy logic in event handlers (defer to next frame if needed)

## Event Definition Guidelines

```csharp
// GOOD: Struct with relevant data
public struct EnemyKilledEvent : IEvent
{
    public readonly int EnemyId;
    public readonly Vector3 Position;
    public readonly int ExperienceReward;
}

// BAD: Class (causes allocation)
public class EnemyKilledEvent : IEvent { }

// BAD: Too much data
public struct EnemyKilledEvent : IEvent
{
    public Enemy FullEnemyReference; // Don't include references!
}
```

## Few-Shot Examples

### Example 1: UI Reacting to Damage
**User**: "Update health bar when player takes damage without coupling."

**Agent**:
```csharp
// In PlayerHealth.cs
public void TakeDamage(float amount)
{
    _currentHealth -= amount;
    EventBus.Publish(new PlayerDamagedEvent 
    { 
        DamageAmount = amount,
        CurrentHealth = _currentHealth,
        MaxHealth = _maxHealth
    });
}

// In HealthBarUI.cs : EventListenerBase<PlayerDamagedEvent>
protected override void OnEventReceived(PlayerDamagedEvent evt)
{
    _slider.value = evt.CurrentHealth / evt.MaxHealth;
}
```

### Example 2: Achievement System
**User**: "Unlock achievement when player kills 100 enemies."

**Agent**:
```csharp
// Subscribe to EnemyKilledEvent
// Track kill count, check threshold, show achievement
```

### Example 3: Sound Effects
**User**: "Play death sound when any enemy dies."

**Agent**:
```csharp
// AudioManager subscribes to EnemyKilledEvent
// Plays sound at event.Position
```

## Related Skills
- `@advanced-design-patterns` - Observer pattern fundamentals
- `@scriptableobject-architecture` - SO-based event channels alternative
- `@di-container-manager` - For injecting event-dependent services

## Template Files
- `templates/EventBus.cs.txt` - Core event bus implementation
- `templates/GameEvents.cs.txt` - Example event definitions
- `templates/EventListenerBase.cs.txt` - Auto-lifecycle listener