---
name: cinemachine-specialist
description: "Unity Cinemachine specialist for dynamic cameras, cutscenes, and cinematic gameplay."
version: 2.0.0
tags: ["visuals", "camera", "Cinemachine", "cutscenes", "Timeline"]
argument-hint: "camera_type='FreeLook' OR blend='EaseInOut' follow='Player'"
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

# Cinemachine Specialist

## Overview
Unity Cinemachine for dynamic camera systems. Build follow cameras, free-look, cutscenes, and cinematic transitions without code.

## When to Use
- Use for third-person follow cameras
- Use for free-look/orbit cameras
- Use for cutscenes with Timeline
- Use for camera transitions/blends
- Use for screen shake and impulse

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   CINEMACHINE SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  VIRTUAL CAMERAS        CINEMACHINE BRAIN      MAIN CAM    │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │ VCam Follow  │─────▶│              │─────▶│          │  │
│  │ VCam FreeLook│─────▶│   Blending   │─────▶│  Output  │  │
│  │ VCam State   │─────▶│   Priority   │─────▶│          │  │
│  │ VCam Target  │─────▶│              │─────▶│          │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         ↑                                                   │
│  [Follow + LookAt targets]                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Virtual Camera Types

| Type | Use Case |
|------|----------|
| **Virtual Camera** | Simple follow/look |
| **FreeLook** | Third-person orbit (3 rigs) |
| **State-Driven** | Animation-based switching |
| **Blend List** | Sequenced cameras |
| **Clear Shot** | Auto-select best view |
| **Target Group** | Multi-target framing |

## Common Setups

| Setup | Components |
|-------|------------|
| **Third-Person** | FreeLook + Framing Transposer |
| **First-Person** | VCam + POV aim |
| **Top-Down** | VCam + Fixed offset |
| **Side-Scroller** | VCam + Framing + Confiner |
| **Cutscene** | Dolly Track + Timeline |

## Best Practices
- ✅ Use Virtual Cameras, not Main Camera transforms
- ✅ Use Cinemachine Brain for blending
- ✅ Set priorities for camera switching
- ✅ Use Confiner for level bounds
- ✅ Use Impulse for screen shake
- ❌ **NEVER** animate Main Camera directly
- ❌ **NEVER** disable Cinemachine Brain during play
- ❌ **NEVER** use too many active VCams

## Few-Shot Examples

### Example 1: Third-Person Camera
**User**: "Create a third-person follow camera."

**Agent**:
```
Setup:
1. Add CinemachineFreeLook to scene
2. Assign Player as Follow & LookAt
3. Configure 3 Orbits (Top/Middle/Bottom):
   - Top: Height 4, Radius 3
   - Middle: Height 2, Radius 5
   - Bottom: Height 0, Radius 4
4. Body: Orbital Transposer
5. Aim: Composer (Dead zone 0.1)
```

### Example 2: Camera Shake
**User**: "Add screen shake on damage."

**Agent**:
```csharp
// Setup: CinemachineImpulseSource on damage dealer
[SerializeField] private CinemachineImpulseSource _impulse;

public void OnDamage(float damage)
{
    _impulse.GenerateImpulse(damage * 0.1f);
}
```
```
Impulse Listener on VCam:
- Gain: 1
- Use 2D Distance: true (for 2D)
```

### Example 3: Cutscene Camera
**User**: "Create a cutscene with dolly."

**Agent**:
```
1. Create CinemachineSmoothPath
2. Place waypoints along desired path
3. Create VCam with TrackedDolly body
4. Set path and Auto Dolly
5. In Timeline:
   - Add Cinemachine Track
   - Create clip for dolly VCam
   - Animate path position
```

## Timeline Integration
- Use Cinemachine Track for blending
- Use Activation clips for VCam switching
- Use Shot clips for specific camera views
- Blend curves control transitions



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void CinemachineSpecialist_Should{ExpectedBehavior}_When{Condition}()
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
public void CinemachineSpecialist_ShouldHandle{EdgeCase}()
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
public void CinemachineSpecialist_ShouldThrow_When{InvalidInput}()
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
- `@juice-game-feel` - Camera feedback
- `@procedural-animation-ik` - Camera follow motion
- `@lighting-post-processing` - DOF integration
