---
name: service-locator-pattern
description: "Implements a lightweight, type-safe Service Locator as a decoupling bridge. Includes a decision matrix for choosing between Service Locator, DI Container, and ScriptableObject Events."
version: 2.0.0
tags: ["architecture", "service-locator", "dependency-management", "decoupling", "SOLID"]
argument-hint: "action='implement' OR action='register' service='IAudioService'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: false
  check_render_pipeline: false
  scan_manifest_for:
    - "com.unity.vcontainer"
    - "com.neuecc.unirx"
performance_budget:
  gc_alloc_per_frame: "0 bytes (dictionary lookup is O(1))"
  max_update_cost: "O(1) — resolve at Awake, cache reference"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Service Locator Pattern

## Overview
The **Service Locator** is a centralized registry of service interfaces. A consumer asks the Locator for `IAudioService` without knowing *which concrete class* implements it. This decouples systems without the setup complexity of a full DI Container. Use it as a stepping-stone when DI Containers are overkill, or when a project has no DI framework installed.

## When to Use

### Decision Matrix

| Scenario | Best Tool |
|---------|-----------|
| Simple game, ≤3 cross-system dependencies | **Service Locator** ✅ |
| Solo/small team, no DI experience | **Service Locator** ✅ |
| Complex game, many cross-system dependencies | **DI Container (VContainer)** — use `@di-container-manager` |
| Gameplay events / cross-scene communication | **ScriptableObject Events** — use `@event-bus-system` |
| Only 1-2 consumers of a service | **Direct reference injection** (no locator needed) |
| Testing requires mock services | **Service Locator** ✅ (easy mock swap) OR **DI Container** |

**Anti-Pattern Warning**: Using a Service Locator heavily (>10 services) becomes a code smell — migrate to VContainer. The Locator is a bridge, not a foundation.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                SERVICE LOCATOR PATTERN                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  REGISTRATION (at boot)         RESOLUTION              │
│  ┌──────────────────────┐       ┌───────────────────┐  │
│  │   GameBootstrapper   │       │ AudioController   │  │
│  │                      │       │                   │  │
│  │ ServiceLocator       │       │ _audio = Service  │  │
│  │  .Register<IAudioSvc>│       │  Locator          │  │
│  │  (new AudioService())│       │  .Get<IAudioSvc>()│  │
│  └──────────────────────┘       └───────────────────┘  │
│              │                          │               │
│              ▼                          ▼               │
│     ┌────────────────────────────────────────────────┐  │
│     │           ServiceLocator<T>                    │  │
│     │  Dictionary<Type, object> _services            │  │
│     │  Register<T>(T service) where T : class        │  │
│     │  Get<T>() where T : class                      │  │
│     │  Unregister<T>()                               │  │
│     └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## TDD Contract

```csharp
// Write these tests BEFORE implementing:
[Test]
public void Register_WhenServiceRegistered_GetReturnsIt()
{
    var mockAudio = new MockAudioService();
    ServiceLocator.Register<IAudioService>(mockAudio);

    var resolved = ServiceLocator.Get<IAudioService>();

    Assert.AreEqual(mockAudio, resolved);
    ServiceLocator.Unregister<IAudioService>();
}

[Test]
public void Get_WhenServiceNotRegistered_ThrowsException()
{
    Assert.Throws<KeyNotFoundException>(() => ServiceLocator.Get<IAudioService>());
}
```

## Procedure

1.  **Define Interfaces**: Create `IAudioService`, `ISaveService`, etc. in a `Services/Interfaces/` folder.
2.  **Implement Concrete Classes**: `AudioService : MonoBehaviour, IAudioService`.
3.  **Create Bootstrapper**: A single `GameBootstrapper.cs` registers all services on `Awake()` in execution order (-100).
4.  **Resolve at Awake**: Consumers call `ServiceLocator.Get<IService>()` in their own `Awake()` or `Start()`.
5.  **Cache the Reference**: Store the resolved service in a private field. Never call `Get<T>()` in `Update()`.

## Best Practices

- ✅ **Register before consuming**: Use `[DefaultExecutionOrder(-100)]` on Bootstrapper.
- ✅ Cache resolved services in `Awake()`: `_audio = ServiceLocator.Get<IAudioService>()`.
- ✅ Use for cross-cutting concerns: Audio, Saving, Analytics, Localization.
- ✅ Swap mock services in Edit Mode tests for easy TDD.
- ❌ **NEVER** call `ServiceLocator.Get<T>()` inside `Update()` — it's a dictionary lookup every frame.
- ❌ **NEVER** register a service more than once without calling `Unregister` first.
- ❌ **NEVER** use more than ~8 services — at that scale, migrate to `@di-container-manager`.

## Few-Shot Examples

### Example 1: Core Implementation
**User**: "Implement a Service Locator for my game."

**Agent**:
```csharp
// ServiceLocator.cs — place anywhere, no MonoBehaviour needed
using System;
using System.Collections.Generic;

public static class ServiceLocator
{
    private static readonly Dictionary<Type, object> _services = new();

    public static void Register<T>(T service) where T : class
    {
        var key = typeof(T);
        if (_services.ContainsKey(key))
            throw new InvalidOperationException($"Service {key.Name} is already registered. Call Unregister first.");
        _services[key] = service;
    }

    public static T Get<T>() where T : class
    {
        var key = typeof(T);
        if (!_services.TryGetValue(key, out var service))
            throw new KeyNotFoundException($"Service {key.Name} not registered. Did you call Register<T>() in Bootstrapper?");
        return (T)service;
    }

    public static bool TryGet<T>(out T service) where T : class
    {
        if (_services.TryGetValue(typeof(T), out var raw))
        {
            service = (T)raw;
            return true;
        }
        service = null;
        return false;
    }

    public static void Unregister<T>() where T : class => _services.Remove(typeof(T));

    public static void Clear() => _services.Clear(); // Use in test teardown
}
```

### Example 2: Bootstrapper
```csharp
// GameBootstrapper.cs
using UnityEngine;

[DefaultExecutionOrder(-100)] // Runs before all other Awake calls
public class GameBootstrapper : MonoBehaviour
{
    [SerializeField] private AudioService _audioService;
    [SerializeField] private SaveSystem _saveSystem;

    private void Awake()
    {
        ServiceLocator.Register<IAudioService>(_audioService);
        ServiceLocator.Register<ISaveService>(_saveSystem);
        DontDestroyOnLoad(gameObject);
    }

    private void OnDestroy()
    {
        ServiceLocator.Clear();
    }
}
```

### Example 3: Consumer
```csharp
// PlayerController.cs
public class PlayerController : MonoBehaviour
{
    private IAudioService _audio;

    private void Awake()
    {
        // Resolve ONCE, cache forever
        _audio = ServiceLocator.Get<IAudioService>();
    }

    private void OnJump()
    {
        _audio.PlayOneShot(AudioClipId.Jump);
    }
}
```

## Related Skills

- `@di-container-manager` — Upgrade path when Service Locator outgrows its scope
- `@event-bus-system` — Alternative for broadcast communication (no direct reference needed)
- `@advanced-game-bootstrapper` — Bootstrapper lifecycle management
- `@automated-unit-testing` — Mock service injection for TDD

## Template Files

- `templates/ServiceLocator.cs.txt` — Static registry implementation
- `templates/GameBootstrapper.cs.txt` — Registration entry point
- `templates/IServiceExample.cs.txt` — Sample service interface
