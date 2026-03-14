---
name: dynamic-audio-mixers
description: "Advanced Unity AudioMixer configuration for dynamic audio effects, snapshots, and ducking."
version: 2.0.0
tags: ["audio", "AudioMixer", "snapshots", "ducking", "effects"]
argument-hint: "mixer_action='snapshot' OR group='Music' effect='lowpass'"
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

# Dynamic Audio Mixers

## Overview
Advanced AudioMixer configuration and runtime control. Covers snapshots, ducking, exposed parameters, and real-time audio effects.

## When to Use
- Use for volume control (settings menus)
- Use for audio ducking (dialogue/music)
- Use for context-based snapshots (underwater, combat)
- Use for dynamic effects (lowpass, reverb zones)
- Use for optimized audio pooling

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AUDIO MIXER HIERARCHY                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                      [MASTER]                               │
│                         │                                   │
│      ┌──────────┬───────┴───────┬──────────┐               │
│      ▼          ▼               ▼          ▼               │
│  [MUSIC]    [SFX]          [AMBIENT]   [VOICE]            │
│      │          │               │          │               │
│  ┌───┴───┐  ┌───┴───┐      ┌───┴───┐     │               │
│  Low Med  UI Combat       Nature  City                     │
│                                                             │
│  SNAPSHOTS: [Default] [Combat] [Pause] [Underwater]        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

| Feature | Use |
|---------|-----|
| **Groups** | Organize audio by type |
| **Exposed Parameters** | Runtime volume control |
| **Snapshots** | Preset mixer states |
| **Send/Receive** | Shared effects (reverb bus) |
| **Effects** | Lowpass, EQ, Compressor |

## Common Patterns

| Pattern | Implementation |
|---------|----------------|
| **Volume Settings** | Expose group volume, use slider |
| **Dialogue Ducking** | Snapshot lowers music during voice |
| **Underwater** | Lowpass + Reverb snapshot |
| **Pause Menu** | Snapshot pauses SFX, keeps music |
| **Combat** | Snapshot boosts impact sounds |

## Best Practices
- ✅ Expose Master, Music, SFX, Voice volumes
- ✅ Use dB logarithmic conversion for sliders
- ✅ Create snapshots for different contexts
- ✅ Use Send for shared reverb effects
- ✅ Transition between snapshots smoothly
- ❌ **NEVER** hardcode volume values
- ❌ **NEVER** skip the mixer hierarchy
- ❌ **NEVER** use linear 0-1 directly for volume

## Few-Shot Examples

### Example 1: Volume Slider
**User**: "Connect slider to music volume."

**Agent**:
```csharp
[SerializeField] private AudioMixer _mixer;
[SerializeField] private Slider _musicSlider;

private void Start()
{
    _musicSlider.onValueChanged.AddListener(SetMusicVolume);
}

public void SetMusicVolume(float value)
{
    // Convert 0-1 to -80dB to 0dB
    float dB = value > 0.001f ? Mathf.Log10(value) * 20f : -80f;
    _mixer.SetFloat("MusicVolume", dB);
}
```

### Example 2: Dialogue Ducking
**User**: "Lower music when character speaks."

**Agent**:
```csharp
// Create "Ducking" snapshot with Music at -10dB

public void StartDialogue()
{
    _mixer.TransitionToSnapshots(
        new[] { _duckingSnapshot }, 
        new[] { 1f }, 
        0.3f);
}

public void EndDialogue()
{
    _mixer.TransitionToSnapshots(
        new[] { _defaultSnapshot }, 
        new[] { 1f }, 
        0.5f);
}
```

### Example 3: Underwater Effect
**User**: "Muffle audio when player is underwater."

**Agent**:
```csharp
// Create "Underwater" snapshot:
// - Master: Lowpass Cutoff 800Hz
// - Add Reverb: Wet 30%

public void EnterWater()
{
    _mixer.TransitionToSnapshots(
        new[] { _underwaterSnapshot }, 
        new[] { 1f }, 
        0.5f);
}
```

## Volume Conversion Formula
```csharp
// Linear 0-1 to Decibels -80 to 0
float LinearToDecibel(float linear) 
    => linear > 0.0001f ? Mathf.Log10(linear) * 20f : -80f;

// Decibels to Linear 0-1
float DecibelToLinear(float dB) 
    => Mathf.Pow(10f, dB / 20f);
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void DynamicAudioMixers_Should{ExpectedBehavior}_When{Condition}()
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
public void DynamicAudioMixers_ShouldHandle{EdgeCase}()
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
public void DynamicAudioMixers_ShouldThrow_When{InvalidInput}()
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
- `@audio-soundscape-architect` - Core audio system
- `@juice-game-feel` - Audio feedback
- `@save-load-serialization` - Persist volume settings
