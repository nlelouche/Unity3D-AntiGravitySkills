---
name: replay-system
description: "Implements a deterministic input-based replay system for Unity. Records player inputs per frame to a timeline, then re-feeds them for perfect playback, death-cam, or automated QA."
version: 2.0.0
tags: ["gameplay", "replay", "determinism", "qa", "death-cam", "input-recording", "debugging"]
argument-hint: "action='record|replay|export' mode='gameplay|death-cam|qa'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.unity.inputsystem"
context_discovery:
  check_unity_version: false
  check_render_pipeline: false
  scan_manifest_for:
    - "com.unity.inputsystem"
performance_budget:
  gc_alloc_per_frame: "< 32 bytes (one InputFrame struct per frame)"
  max_update_cost: "O(1) — struct copy per frame"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - write_to_file
---

# Replay System

## Overview
A **deterministic replay system** records player inputs (not game state) to a timeline. On playback, the same inputs are re-injected into the game simulation, which reproduces the exact same result — this is far lighter than recording full game state. Use cases: **death cameras** (play the last N seconds when the player dies), **automated QA** (record a playthrough and replay it to detect bugs), and **speedrun validation**.

> [!IMPORTANT]
> This approach requires **deterministic simulation** — same inputs → same result. Avoid random values not derived from a seeded RNG during gameplay.

## When to Use
- Use for **death cameras** showing how the player died.
- Use for **automated regression QA** — record a session, replay on every build.
- Use for **speedrun ghost** / spectator replay.
- ❌ Do NOT use for online multiplayer rollback netcode — use a dedicated netcode library.

## Architecture

```
RECORDING MODE:
  Input System → InputFrame captured → InputTimeline.Frames[]
                                               │
                                               ▼
                                        [ [F0][F1][F2]...[FN] ]

PLAYBACK MODE:
  InputTimeline.Frames[] → re-injected to game → identical simulation
```

## Core Implementation

```csharp
// --- InputFrame.cs (unmanaged struct — zero GC) ---
using System.Runtime.InteropServices;
using UnityEngine;

[StructLayout(LayoutKind.Sequential)]
public struct InputFrame
{
    public int    FrameIndex;
    public float  Time;
    public Vector2 Move;
    public Vector2 Look;
    public bool   Jump;
    public bool   Fire;
    public bool   Sprint;
}

// --- InputTimeline.cs ---
using System.Collections.Generic;

public class InputTimeline
{
    private readonly List<InputFrame> _frames = new(3600); // pre-alloc for 60s at 60fps
    public IReadOnlyList<InputFrame> Frames => _frames;
    public int FrameCount => _frames.Count;

    public void Record(in InputFrame frame) => _frames.Add(frame);
    public void Clear() => _frames.Clear();

    public InputFrame GetFrame(int index) =>
        (index >= 0 && index < _frames.Count) ? _frames[index] : default;
}

// --- ReplaySystem.cs ---
using UnityEngine;
using UnityEngine.InputSystem;

public class ReplaySystem : MonoBehaviour
{
    public enum Mode { Idle, Recording, Replaying }

    private Mode          _mode = Mode.Idle;
    private InputTimeline _timeline = new();
    private int           _playbackFrame;

    // Inject your player's actual input provider
    public IInputProvider InputProvider { get; set; }

    public bool IsRecording  => _mode == Mode.Recording;
    public bool IsReplaying  => _mode == Mode.Replaying;

    public void StartRecording()
    {
        _timeline.Clear();
        _mode = Mode.Recording;
        Debug.Log("[Replay] Recording started");
    }

    public void StopRecording()
    {
        _mode = Mode.Idle;
        Debug.Log($"[Replay] Recorded {_timeline.FrameCount} frames");
    }

    public void StartPlayback()
    {
        _playbackFrame = 0;
        _mode          = Mode.Replaying;
        Debug.Log("[Replay] Playback started");
    }

    private void FixedUpdate()
    {
        if (_mode == Mode.Recording && InputProvider != null)
        {
            _timeline.Record(new InputFrame
            {
                FrameIndex = Time.frameCount,
                Time       = Time.time,
                Move       = InputProvider.MoveInput,
                Look       = InputProvider.LookInput,
                Jump       = InputProvider.JumpPressed,
                Fire       = InputProvider.FirePressed,
                Sprint     = InputProvider.SprintHeld
            });
        }
        else if (_mode == Mode.Replaying)
        {
            if (_playbackFrame >= _timeline.FrameCount)
            { _mode = Mode.Idle; return; }

            var frame = _timeline.GetFrame(_playbackFrame++);
            InputProvider?.InjectFrame(frame); // Re-feed to simulation
        }
    }
}

// --- IInputProvider.cs ---
public interface IInputProvider
{
    Vector2 MoveInput   { get; }
    Vector2 LookInput   { get; }
    bool    JumpPressed { get; }
    bool    FirePressed { get; }
    bool    SprintHeld  { get; }
    void    InjectFrame(in InputFrame frame);
}
```

## Death Camera Integration

```csharp
// On player death: play back the last 5 seconds
public class DeathCameraController : MonoBehaviour
{
    [SerializeField] private ReplaySystem _replay;
    [SerializeField] private float        _deathCamDuration = 5f;

    public void OnPlayerDeath()
    {
        // Trim timeline to last N seconds
        // TODO: implement TrimToLastSeconds(float seconds) on InputTimeline
        _replay.StopRecording();
        StartCoroutine(PlayDeathCam());
    }

    private System.Collections.IEnumerator PlayDeathCam()
    {
        _replay.StartPlayback();
        yield return new WaitUntil(() => !_replay.IsReplaying);
        // Return control to player / show respawn UI
    }
}
```

## TDD Contract

```csharp
[Test]
public void InputTimeline_Record_StoresFrames()
{
    var timeline = new InputTimeline();
    timeline.Record(new InputFrame { FrameIndex = 0, Jump = true });
    timeline.Record(new InputFrame { FrameIndex = 1, Fire = true });

    Assert.AreEqual(2, timeline.FrameCount);
    Assert.IsTrue(timeline.GetFrame(0).Jump);
    Assert.IsTrue(timeline.GetFrame(1).Fire);
}

[Test]
public void InputTimeline_Clear_ResetsCount()
{
    var timeline = new InputTimeline();
    timeline.Record(new InputFrame { FrameIndex = 0 });
    timeline.Clear();
    Assert.AreEqual(0, timeline.FrameCount);
}
```

## Best Practices

- ✅ Use **`FixedUpdate`** for frame capture — deterministic timing.
- ✅ Pre-allocate `InputTimeline` with expected capacity to avoid resizing.
- ✅ Use **seeded RNG** for all gameplay randomness to maintain determinism.
- ✅ Serialize `InputTimeline` to JSON/binary for QA regression files.
- ❌ **NEVER** record absolute game state (position, HP) — record inputs only.
- ❌ **NEVER** use `Time.deltaTime` during playback; use the recorded timestamp.

## Related Skills

- `@save-load-serialization` — Export replay files to disk
- `@automated-unit-testing` — Use replay files as integration test drivers
- `@analytics-heatmaps` — Feed replay data into heatmap analytics
