---
name: dynamic-audio-mixers
description: Generates Audio Managers, handled via Pooling and AudioMixers. Use to "play sound", "setup audio", or "background music".
argument-hint: "name='SoundManager' namespace='Game.Audio'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Dynamic Audio Mixers

## Goal
To implement a performant Audio System that doesn't stutter when 50 explosions happen at once. We use **Object Pooling** for AudioSources.

## Architecture
- **AudioManager**: Singleton/Service that manages the pool.
- **Mixers**: Exposed parameters for Volume Control (UI).

## Procedure
1.  **Generate Manager**: `AudioManager.cs` with pooling logic.
2.  **Instruction**: Assign an AudioMixer Group to the prefab.

## Few-Shot Example
User: "I need sound for my game."
Agent: Generates `SoundManager.cs`. "Attach this to a persistence object."
