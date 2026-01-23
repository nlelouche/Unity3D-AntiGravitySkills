---
name: di-container-manager
description: "Dependency Injection specialist for decoupled, testable Unity architectures using DI containers."
version: 1.0.0
tags: ["architecture", "DI", "dependency-injection", "IoC", "VContainer", "Zenject"]
argument-hint: "container='VContainer' service='IAudioService'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# DI Container Manager

## Overview
Dependency Injection for Unity. Create loosely coupled, testable systems where dependencies are injected rather than created directly.

## When to Use
- Use when classes need external dependencies
- Use when implementing testable architecture
- Use when replacing global singletons
- Use when building modular systems
- Use when mocking services for unit tests

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DI CONTAINER                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Register                          Resolve                  │
│  ┌──────────────┐                 ┌──────────────┐         │
│  │ IAudioService│ ──────────────▶ │ AudioManager │         │
│  │ IInputService│ ──────────────▶ │ InputManager │         │
│  │ ISaveService │ ──────────────▶ │ SaveManager  │         │
│  └──────────────┘                 └──────────────┘         │
│         ↓                                                   │
│  ┌──────────────────────────────────────────────────┐      │
│  │                   PlayerController               │      │
│  │  [Inject] IAudioService _audio;                  │      │
│  │  [Inject] IInputService _input;                  │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Popular DI Containers

| Container | Features | Recommended |
|-----------|----------|:-----------:|
| **VContainer** | Fast, lightweight, Unity-optimized | ✅ |
| **Zenject** | Feature-rich, mature | ✅ |
| **Extenject** | Zenject fork, maintained | ✅ |
| **Manual DI** | No container, constructor injection | ⚠️ |

## Injection Types
- **Constructor**: Preferred for required deps
- **Field/Property**: `[Inject]` attribute
- **Method**: `[Inject]` on method

## Best Practices
- ✅ Program to interfaces, not implementations
- ✅ Register in composition root (Installer)
- ✅ Keep containers focused (per scene/feature)
- ✅ Use `[Inject]` sparingly, prefer constructor
- ✅ Singleton for managers, Transient for instances
- ❌ **NEVER** use Service Locator pattern inside classes
- ❌ **NEVER** inject container itself (hidden deps)
- ❌ **NEVER** create circular dependencies

## Few-Shot Examples

### Example 1: VContainer Registration
**User**: "Register audio and save services."

**Agent**:
```csharp
public class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<AudioManager>(Lifetime.Singleton).As<IAudioService>();
        builder.Register<SaveManager>(Lifetime.Singleton).As<ISaveService>();
        
        builder.RegisterComponentInHierarchy<PlayerController>();
    }
}
```

### Example 2: Injection
**User**: "Inject dependencies into PlayerController."

**Agent**:
```csharp
public class PlayerController : MonoBehaviour
{
    [Inject] private readonly IAudioService _audio;
    [Inject] private readonly ISaveService _save;
    
    public void TakeDamage(float amount)
    {
        _audio.PlaySound("hit");
        _save.AutoSave();
    }
}
```

### Example 3: Unit Testing
**User**: "Mock audio service for tests."

**Agent**:
```csharp
public class MockAudioService : IAudioService
{
    public bool WasSoundPlayed { get; private set; }
    public void PlaySound(string id) => WasSoundPlayed = true;
}

// In test
var player = new PlayerController(new MockAudioService());
player.TakeDamage(10);
Assert.IsTrue(mockAudio.WasSoundPlayed);
```

## Lifetimes
- **Singleton**: One instance for container lifetime
- **Scoped**: One instance per scope (scene)
- **Transient**: New instance every resolve

## Related Skills
- `@interface-driven-development` - Interfaces for DI
- `@advanced-game-bootstrapper` - Initialization order
- `@advanced-design-patterns` - Factory with DI

## Recommended Package
```
VContainer - https://github.com/hadashiA/VContainer
```
Fastest DI container for Unity with minimal allocation.
