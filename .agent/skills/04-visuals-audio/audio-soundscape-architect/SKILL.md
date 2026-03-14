---
name: audio-soundscape-architect
description: "Unity audio system specialist for immersive soundscapes, music, and audio management."
version: 2.0.0
tags: ["audio", "sound", "music", "AudioMixer", "FMOD", "Wwise"]
argument-hint: "sound_type='sfx' OR mixer_group='Music' ducking='true'"
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

# Audio & Soundscape Architect

## Overview
Unity audio systems for immersive soundscapes. Covers AudioSource, AudioMixer, spatial audio, and integration with middleware (FMOD, Wwise).

## When to Use
- Use when implementing game audio systems
- Use when setting up spatial 3D audio
- Use when creating AudioMixer setups
- Use when managing music transitions
- Use when optimizing audio performance

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AUDIO SYSTEM                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  AUDIO SOURCES         AUDIO MIXER         OUTPUT           │
│  ┌──────────┐         ┌──────────┐        ┌──────────┐     │
│  │ SFX      │────────▶│ SFX Group│───────▶│          │     │
│  │ Music    │────────▶│Music Grp │───────▶│  Master  │     │
│  │ Ambient  │────────▶│Ambient Gr│───────▶│          │     │
│  │ Voice    │────────▶│Voice Grp │───────▶│          │     │
│  └──────────┘         └──────────┘        └──────────┘     │
│                             │                               │
│                       [Effects]                             │
│                    Lowpass, Reverb                          │
│                    Ducking, Compress                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Audio Categories

| Category | Use | Settings |
|----------|-----|----------|
| **SFX** | One-shot effects | 2D/3D, pooled |
| **Music** | Background tracks | Loop, crossfade |
| **Ambient** | Environment | 3D spatial, loop |
| **Voice** | Dialogue, narration | Priority, ducking |
| **UI** | Interface feedback | 2D, low latency |

## AudioMixer Best Practices

| Feature | Purpose |
|---------|---------|
| **Groups** | Organize audio types |
| **Snapshots** | Preset mixer states |
| **Ducking** | Lower music during dialogue |
| **Exposed Parameters** | Runtime volume control |
| **Send/Receive** | Shared effects (reverb) |

## Best Practices
- ✅ Use object pooling for frequent SFX
- ✅ Use AudioMixer groups for volume control
- ✅ Compress audio appropriately (Vorbis/ADPCM)
- ✅ Use spatial blend for 3D positioning
- ✅ Implement audio occlusion for realism
- ❌ **NEVER** load all audio at startup
- ❌ **NEVER** use uncompressed audio for large files
- ❌ **NEVER** skip AudioMixer for direct volume

## Few-Shot Examples

### Example 1: Audio Manager Setup
**User**: "Create a simple audio manager."

**Agent**:
```csharp
public class AudioManager : MonoBehaviour
{
    [SerializeField] private AudioMixerGroup _sfxGroup;
    [SerializeField] private AudioMixerGroup _musicGroup;
    
    public void PlaySFX(AudioClip clip, Vector3 position)
    {
        var source = GetPooledSource();
        source.clip = clip;
        source.outputAudioMixerGroup = _sfxGroup;
        source.transform.position = position;
        source.Play();
    }
}
```

### Example 2: Music Crossfade
**User**: "Fade between music tracks."

**Agent**:
```csharp
public async UniTask CrossfadeMusic(AudioClip newTrack, float duration)
{
    var fadeOut = _currentSource.DOFade(0, duration).ToUniTask();
    _nextSource.clip = newTrack;
    _nextSource.volume = 0;
    _nextSource.Play();
    var fadeIn = _nextSource.DOFade(1, duration).ToUniTask();
    await UniTask.WhenAll(fadeOut, fadeIn);
    (_currentSource, _nextSource) = (_nextSource, _currentSource);
}
```

### Example 3: Ducking Setup
**User**: "Lower music during dialogue."

**Agent**:
```
AudioMixer setup:
1. Create "Ducking" snapshot
2. Lower Music group by -10dB
3. Expose "MusicVolume" parameter

Code:
_mixer.TransitionToSnapshots(
    new[] { duckingSnapshot }, 
    new[] { 1f }, 
    0.3f);
```

## Middleware Comparison

| Feature | Unity Audio | FMOD | Wwise |
|---------|:-----------:|:----:|:-----:|
| Cost | Free | Indie free | $$ |
| Ease | Easy | Medium | Advanced |
| Features | Basic | Rich | Enterprise |
| 3D Audio | Good | Excellent | Excellent |



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void AudioSoundscapeArchitect_Should{ExpectedBehavior}_When{Condition}()
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
public void AudioSoundscapeArchitect_ShouldHandle{EdgeCase}()
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
public void AudioSoundscapeArchitect_ShouldThrow_When{InvalidInput}()
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
- `@juice-game-feel` - Audio feedback
- `@vfx-graph-shuriken` - Audio-reactive VFX
- `@scriptableobject-architecture` - Audio event SO
