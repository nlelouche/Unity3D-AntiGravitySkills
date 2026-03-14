---
name: automated-unit-testing
description: "Implementation of NUnit tests for Unity, covering EditMode and PlayMode scenarios for reliable code verification."
version: 2.0.0
tags: ["testing", "nunit", "qa", "validation", "tdd"]
argument-hint: "test_type='PlayMode' OR context='InventorySystem' coverage='strict'"
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

# Automated Unit Testing

## Overview
Implementation of automated tests using the Unity Test Framework (NUnit). Ensures code reliability through EditMode (logic) and PlayMode (integration/physics) testing.

## When to Use
- Use when logic is complex (Inventory, Stats)
- Use when refactoring legacy code
- Use when verifying bug fixes (Regression test)
- Use when strictly following TDD
- Use for CI/CD pipelines

## Test Types

| Type | Environment | Time Scale | Use Case |
|------|-------------|------------|----------|
| **EditMode** | Editor | Instant | Pure C# logic, Math, Data parsing |
| **PlayMode** | Runtime | Real-time | Physics, Coroutines, Visuals, UI |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TESTING FRAMEWORK                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ASSEMBLY DEFINITION (.asmdef)                              │
│  ┌──────────────────────┐                                   │
│  │ Game.Tests.asmdef    │                                   │
│  │ [x] Test Assemblies  │                                   │
│  │ Refs: Game.asmdef    │                                   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│             ▼                                               │
│  TEST SCRIPT                                                │
│  ┌──────────────────────┐                                   │
│  │ [TestFixture]        │                                   │
│  │ InventoryTests       │                                   │
│  │  ├─ [SetUp]          │                                   │
│  │  ├─ [Test] AddItem   │                                   │
│  │  └─ [TearDown]       │                                   │
│  └──────────────────────┘                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Create separate `.asmdef` for Tests
- ✅ Use `[SetUp]` and `[TearDown]` for state cleanup
- ✅ Name tests clearly: `MethodName_Condition_ExpectedResult`
- ✅ Mock dependencies where possible (Interfaces)
- ✅ Keep tests independent of each other
- ❌ **NEVER** test private methods (test public behavior)
- ❌ **NEVER** use `GameObject.Find` in tests (slow/fragile)
- ❌ **NEVER** rely on previous test state

## Few-Shot Examples

### Example 1: EditMode Test (Pure Logic)
**User**: "Test health calculation."

**Agent**:
```csharp
using NUnit.Framework;

public class HealthTests
{
    [Test]
    public void TakeDamage_PositiveAmount_ReducesHealth()
    {
        // Arrange
        var health = new HealthSystem(100);

        // Act
        health.TakeDamage(10);

        // Assert
        Assert.AreEqual(90, health.CurrentHealth);
    }

    [Test]
    public void TakeDamage_ExceedingCurrent_HealthZero()
    {
        // Arrange
        var health = new HealthSystem(10);

        // Act
        health.TakeDamage(20);

        // Assert
        Assert.AreEqual(0, health.CurrentHealth);
        Assert.IsTrue(health.IsDead);
    }
}
```

### Example 2: PlayMode Test (Unity Integration)
**User**: "Test player movement physics."

**Agent**:
```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public class PlayerMovementTests
{
    private GameObject _playerGO;
    private PlayerController _controller;

    [SetUp]
    public void Setup()
    {
        _playerGO = new GameObject("Player");
        var rb = _playerGO.AddComponent<Rigidbody>();
        _controller = _playerGO.AddComponent<PlayerController>();
    }

    [UnityTest]
    public IEnumerator Move_VectorInput_ChangesPosition()
    {
        // Arrange
        var startPos = _playerGO.transform.position;

        // Act
        _controller.Move(Vector3.forward);
        yield return new WaitForSeconds(0.5f); // Wait for physics

        // Assert
        Assert.AreNotEqual(startPos, _playerGO.transform.position);
    }

    [TearDown]
    public void Teardown()
    {
        Object.Destroy(_playerGO);
    }
}
```

### Example 3: Parameterized Tests
**User**: "Test multiple damage values."

**Agent**:
```csharp
[TestCase(10, 90)]
[TestCase(50, 50)]
[TestCase(100, 0)]
public void TakeDamage_VariousAmounts_CalculatesCorrectly(int damage, int expected)
{
    var health = new HealthSystem(100);
    health.TakeDamage(damage);
    Assert.AreEqual(expected, health.CurrentHealth);
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
public void AutomatedUnitTesting_Should{ExpectedBehavior}_When{Condition}()
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
public void AutomatedUnitTesting_ShouldHandle{EdgeCase}()
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
public void AutomatedUnitTesting_ShouldThrow_When{InvalidInput}()
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
- `@unity-mcp-connector` - Run tests via command
- `@custom-editor-scripting` - Test editor tools
- `@oop-patterns-architect` - Design for testability (DI)
