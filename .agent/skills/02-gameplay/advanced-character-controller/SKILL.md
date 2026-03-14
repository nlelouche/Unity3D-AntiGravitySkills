---
name: advanced-character-controller
description: "Complete 3D character controller with ground detection, jumping, slopes, and state-based movement."
version: 2.0.0
tags: ["gameplay", "character", "controller", "movement", "platformer"]
argument-hint: "speed='5' jump_height='2' gravity='-20'"
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

# Advanced Character Controller

## Overview
Complete 3D character controller with robust ground detection, variable jump height, slope handling, coyote time, and state-based movement.

## When to Use
- Use when implementing player movement
- Use when default CharacterController isn't enough
- Use when platformer mechanics are needed
- Use when slopes/stairs need special handling
- Use when movement states are complex

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 CharacterController3D                       │
├─────────────────────────────────────────────────────────────┤
│  Movement: Speed, Acceleration, Deceleration                │
│  Jumping: Height, AirControl, CoyoteTime, JumpBuffer        │
│  Ground: GroundCheck, SlopeLimit, StepOffset                │
│  States: Grounded, Falling, Jumping, Sliding                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Ground Detection                          │
├─────────────────────────────────────────────────────────────┤
│  SphereCast down from feet                                  │
│  Check normal for slope angle                               │
│  Snap to ground on small drops                              │
└─────────────────────────────────────────────────────────────┘
```

## Movement Features

| Feature | Description |
|---------|-------------|
| **Ground Snap** | Stick to ground on small drops |
| **Coyote Time** | Grace period after leaving ground |
| **Jump Buffer** | Queue jump input before landing |
| **Air Control** | Movement while airborne |
| **Slope Limit** | Max walkable angle |
| **Step Offset** | Auto-climb small steps |

## State Machine Integration
```csharp
States:
├── Grounded
│   ├── Idle
│   ├── Walking
│   └── Running
├── Airborne
│   ├── Jumping
│   └── Falling
└── Special
    ├── Sliding
    ├── Climbing
    └── Swimming
```

## Best Practices
- ✅ Use Physics.SphereCast for ground detection
- ✅ Apply gravity in FixedUpdate
- ✅ Implement coyote time (0.1-0.2s)
- ✅ Implement jump buffer (0.1-0.2s)
- ✅ Separate input from movement
- ❌ **NEVER** use transform.Translate for physics
- ❌ **NEVER** check isGrounded only in Update

## Few-Shot Examples

### Example 1: Basic Movement
**User**: "WASD movement with controller."

**Agent**:
```csharp
Vector3 input = new Vector3(Input.GetAxisRaw("Horizontal"), 0, Input.GetAxisRaw("Vertical"));
Vector3 moveDir = transform.TransformDirection(input.normalized);
controller.Move(moveDir * speed * Time.deltaTime);
```

### Example 2: Variable Jump
**User**: "Hold jump for higher jumps."

**Agent**:
```csharp
if (Input.GetButtonDown("Jump") && isGrounded)
    velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);

if (Input.GetButtonUp("Jump") && velocity.y > 0)
    velocity.y *= 0.5f; // Cut jump short
```

### Example 3: Coyote Time
**User**: "Allow jump briefly after leaving ground."

**Agent**:
```csharp
if (isGrounded) coyoteTimer = coyoteTime;
else coyoteTimer -= Time.deltaTime;

bool canJump = coyoteTimer > 0f;
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void AdvancedCharacterController_Should{ExpectedBehavior}_When{Condition}()
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
public void AdvancedCharacterController_ShouldHandle{EdgeCase}()
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
public void AdvancedCharacterController_ShouldThrow_When{InvalidInput}()
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
- `@state-machine-architect` - Movement states
- `@physics-logic` - Ground detection
- `@ability-skill-system` - Movement abilities

## Template Files
Available in templates/ folder.
