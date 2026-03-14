---
name: procedural-animation-ik
description: "Procedural animation and IK specialist for dynamic, responsive character motion."
version: 2.0.0
tags: ["animation", "IK", "procedural", "rigging", "motion"]
argument-hint: "ik_type='foot' OR target='hand' weight='1.0'"
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
  check_render_pipeline: true
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
---

# Procedural Animation & IK

## Overview
Procedural animation and Inverse Kinematics for dynamic, responsive character motion. Foot IK, look-at, hand placement, and runtime motion adaptation.

## When to Use
- Use for foot IK on uneven terrain
- Use for look-at/head tracking
- Use for weapon/item holding
- Use for dynamic leaning/tilting
- Use for procedural locomotion

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  ANIMATION PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ANIMATION CLIP      IK LAYER         FINAL POSE           │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐         │
│  │ Base     │─────▶│ Foot IK  │─────▶│          │         │
│  │ Motion   │      │ Hand IK  │      │ Blended  │         │
│  │ (Clip)   │      │ Look At  │      │ Output   │         │
│  └──────────┘      └──────────┘      └──────────┘         │
│        ↑                 ↑                                  │
│  [Animator]      [OnAnimatorIK]                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## IK Types

| Type | Use Case | Unity Method |
|------|----------|--------------|
| **Foot IK** | Ground adaptation | `SetIKPosition/Rotation` |
| **Hand IK** | Weapon hold, grab | `SetIKPosition/Rotation` |
| **Look At** | Head tracking | `SetLookAtPosition/Weight` |
| **Hint** | Elbow/Knee direction | `SetIKHintPosition` |

## Common Techniques

| Technique | Description |
|-----------|-------------|
| **Foot Placement** | Raycast ground, adjust feet |
| **Body Offset** | Lower body on slopes |
| **Procedural Lean** | Tilt body during turns |
| **Head Look** | Track target with head |
| **Two-Bone IK** | Arms reaching for objects |

## Best Practices
- ✅ Use Animation Rigging package for complex setups
- ✅ Blend IK weights smoothly (lerp)
- ✅ Cache raycast results
- ✅ Use layers for IK in Animator
- ✅ Validate IK targets exist
- ❌ **NEVER** set IK weight to 1 instantly
- ❌ **NEVER** skip ground checks for foot IK
- ❌ **NEVER** apply IK without base animation

## Few-Shot Examples

### Example 1: Foot IK
**User**: "Add foot IK for terrain adaptation."

**Agent**:
```csharp
private void OnAnimatorIK(int layerIndex)
{
    // Left foot
    if (Physics.Raycast(_leftFoot.position + Vector3.up, 
        Vector3.down, out var hitL, 2f, _groundMask))
    {
        _animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, 1f);
        _animator.SetIKRotationWeight(AvatarIKGoal.LeftFoot, 1f);
        _animator.SetIKPosition(AvatarIKGoal.LeftFoot, 
            hitL.point + Vector3.up * _footOffset);
        _animator.SetIKRotation(AvatarIKGoal.LeftFoot,
            Quaternion.LookRotation(transform.forward, hitL.normal));
    }
    // Repeat for right foot
}
```

### Example 2: Look At Target
**User**: "Make character look at target."

**Agent**:
```csharp
[SerializeField] private Transform _lookTarget;
[SerializeField] private float _lookWeight = 0.8f;

private void OnAnimatorIK(int layerIndex)
{
    if (_lookTarget != null)
    {
        _animator.SetLookAtWeight(_lookWeight, 0.3f, 0.7f, 0.5f, 0.5f);
        _animator.SetLookAtPosition(_lookTarget.position);
    }
}
```

### Example 3: Procedural Lean
**User**: "Add lean during movement."

**Agent**:
```csharp
private void Update()
{
    float turnInput = Input.GetAxis("Horizontal");
    float targetLean = -turnInput * _maxLeanAngle;
    _currentLean = Mathf.Lerp(_currentLean, targetLean, 
        Time.deltaTime * _leanSpeed);
    
    _spine.localRotation = Quaternion.Euler(0, 0, _currentLean);
}
```

## Animation Rigging Package
For complex rigs, use Unity's Animation Rigging:
- Multi-Aim Constraint
- Two-Bone IK Constraint
- Chain IK Constraint
- Twist Correction



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void ProceduralAnimationIk_Should{ExpectedBehavior}_When{Condition}()
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
public void ProceduralAnimationIk_ShouldHandle{EdgeCase}()
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
public void ProceduralAnimationIk_ShouldThrow_When{InvalidInput}()
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
- `@advanced-character-controller` - Movement integration
- `@cinemachine-specialist` - Camera follow
- `@juice-game-feel` - Motion polish
