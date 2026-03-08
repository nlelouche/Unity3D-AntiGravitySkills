---
name: oop-patterns-architect
description: "Object-Oriented design patterns specialist for clean, maintainable Unity architectures."
version: 2.0.0
tags: ["architecture", "OOP", "SOLID", "patterns", "clean-code"]
argument-hint: "pattern='Repository' OR principle='SRP'"
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
tdd_first: false
---

# OOP Patterns Architect

## Overview
Object-Oriented Programming patterns for Unity. Apply SOLID principles, clean architecture, and domain-driven design for maintainable codebases.

## When to Use
- Use when designing class hierarchies
- Use when applying SOLID principles
- Use when code smells appear
- Use when building domain models
- Use when refactoring legacy code

## SOLID Principles

| Principle | Summary |
|-----------|---------|
| **S**ingle Responsibility | One class, one reason to change |
| **O**pen/Closed | Open for extension, closed for modification |
| **L**iskov Substitution | Subtypes must be substitutable |
| **I**nterface Segregation | Many specific interfaces > one fat |
| **D**ependency Inversion | Depend on abstractions |

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION                             │
│              (UI, Input, Controllers)                       │
├─────────────────────────────────────────────────────────────┤
│                    APPLICATION                              │
│              (Use Cases, Services)                          │
├─────────────────────────────────────────────────────────────┤
│                      DOMAIN                                 │
│              (Entities, Value Objects)                      │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE                            │
│              (Repositories, External APIs)                  │
└─────────────────────────────────────────────────────────────┘
              Dependencies flow DOWN only
```

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| **Repository** | Abstract data access |
| **Service** | Stateless business logic |
| **Value Object** | Immutable data |
| **Entity** | Identity + lifecycle |
| **Aggregate** | Transaction boundary |

## Best Practices
- ✅ Prefer composition over inheritance
- ✅ Keep classes small and focused
- ✅ Use interfaces for dependencies
- ✅ Separate data from behavior when appropriate
- ✅ Make illegal states unrepresentable
- ❌ **NEVER** inherit more than 2 levels deep
- ❌ **NEVER** use inheritance for code reuse alone
- ❌ **NEVER** expose internal state (encapsulation)

## Few-Shot Examples

### Example 1: SRP Violation Fix
**User**: "This class does too much."

**Agent**:
```csharp
// BEFORE: Violates SRP
public class Player : MonoBehaviour
{
    void Move() { }
    void Attack() { }
    void SaveGame() { }  // ❌ Not player's job
    void RenderUI() { }  // ❌ Not player's job
}

// AFTER: Single responsibility
public class Player : MonoBehaviour
{
    void Move() { }
    void Attack() { }
}
// SaveManager handles saving
// UIManager handles rendering
```

### Example 2: Repository Pattern
**User**: "Abstract database access."

**Agent**:
```csharp
public interface IPlayerRepository
{
    Player GetById(string id);
    void Save(Player player);
    IEnumerable<Player> GetAll();
}

public class LocalPlayerRepository : IPlayerRepository
{
    public Player GetById(string id) => LoadFromFile(id);
    public void Save(Player player) => SaveToFile(player);
    // ...
}

public class CloudPlayerRepository : IPlayerRepository
{
    public Player GetById(string id) => FetchFromServer(id);
    // ...
}
```

### Example 3: Value Object
**User**: "Create immutable currency."

**Agent**:
```csharp
public readonly struct Currency
{
    public int Gold { get; }
    public int Gems { get; }
    
    public Currency(int gold, int gems)
    {
        Gold = gold;
        Gems = gems;
    }
    
    public Currency Add(Currency other) =>
        new Currency(Gold + other.Gold, Gems + other.Gems);
    
    public static Currency operator +(Currency a, Currency b) =>
        a.Add(b);
}
```

## Code Smells to Avoid
- **God Object**: Class that knows/does everything
- **Feature Envy**: Method uses other class's data too much
- **Primitive Obsession**: Using primitives instead of types
- **Long Parameter List**: > 3-4 parameters

## Related Skills
- `@di-container-manager` - Dependency injection
- `@interface-driven-development` - Interface design
- `@advanced-design-patterns` - GoF patterns
