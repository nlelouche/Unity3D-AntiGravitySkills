---
name: advanced-character-controller
description: "Complete 3D character controller with ground detection, jumping, slopes, and state-based movement."
version: 1.0.0
tags: ["gameplay", "character", "controller", "movement", "platformer"]
argument-hint: "speed='5' jump_height='2' gravity='-20'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
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

## Related Skills
- `@state-machine-architect` - Movement states
- `@physics-logic` - Ground detection
- `@ability-skill-system` - Movement abilities

## Template Files
Available in templates/ folder.
