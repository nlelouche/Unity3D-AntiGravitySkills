---
name: di-container-manager
description: "Dependency Injection specialist for decoupled, testable Unity architectures using DI containers."
version: 2.0.0
tags: ["architecture", "DI", "dependency-injection", "IoC", "VContainer", "Zenject"]
argument-hint: "container='VContainer' service='IAudioService'"
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



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void DiContainerManager_Should{ExpectedBehavior}_When{Condition}()
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
public void DiContainerManager_ShouldHandle{EdgeCase}()
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
public void DiContainerManager_ShouldThrow_When{InvalidInput}()
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
- `@interface-driven-development` - Interfaces for DI
- `@advanced-game-bootstrapper` - Initialization order
- `@advanced-design-patterns` - Factory with DI

## Recommended Package
```
VContainer - https://github.com/hadashiA/VContainer
```
Fastest DI container for Unity with minimal allocation.
