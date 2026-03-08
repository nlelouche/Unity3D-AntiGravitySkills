---
name: day-night-cycle
description: "Time progression, directional light rotation, and event triggers for dawn and dusk."
version: 2.0.0
tags: ["gameplay", "day-night", "lighting", "time"]
argument-hint: "action='generate' cycle_minutes='24'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: false
  check_render_pipeline: true
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes"
  max_update_cost: "O(1) - single rotation and check per frame"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Day Night Cycle

## Overview
A robust Day/Night cycle system decoupled from rendering. It rotates a Directional Light to simulate the sun, tracks in-game time (0-24 hours), and fires C# events when time-of-day phases change (e.g., Dawn, Noon, Dusk, Midnight).

## When to Use
- Use for open-world games with dynamic time.
- Use for farming or survival games where days matter.
- Use to trigger logic based on time (shops closing, enemies spawning).
- ❌ Do NOT use for staticly lit scenes or indoor-only levels.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DAY NIGHT CYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TIME TRACKER                 LIGHT CONTROLLER              │
│  ┌────────────────┐           ┌───────────────────────────┐ │
│  │ Tick()         │──────────▶│ UpdateRotation()          │ │
│  │ CurrentTime    │           │ UpdateIntensity()         │ │
│  │ OnDayPassed    │           └───────────────────────────┘ │
│  └────────────────┘                                         │
│          │                                                  │
│          ▼ (Events)                                         │
│  ┌────────────────┐                                         │
│  │ World Events   │ (Spawn monsters, close shops)           │
│  └────────────────┘                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## TDD Contract

```csharp
[Test]
public void TimePasses_AccordingToTimeScale()
{
    var timeSystem = new TimeSystem(dayLengthInSeconds: 60f);
    timeSystem.Tick(15f); // Advance 1/4 of a day
    Assert.AreEqual(6f, timeSystem.CurrentHour); // 6 AM
}

[Test]
public void TimePassesMidnight_RaisesDayPassedEvent()
{
    var timeSystem = new TimeSystem(dayLengthInSeconds: 60f);
    timeSystem.SetTime(23f); // 11 PM
    
    bool eventRaised = false;
    timeSystem.OnDayPassed += () => eventRaised = true;
    
    timeSystem.Tick(5f); // Pass midnight
    
    Assert.IsTrue(eventRaised);
    Assert.AreEqual(1f, timeSystem.CurrentHour); // 1 AM
}
```

## Core Implementation

```csharp
// --- TimeSystem.cs ---
using System;
using UnityEngine;

public class TimeSystem : MonoBehaviour
{
    [Header("Settings")]
    [Tooltip("How many real-world minutes a full in-game day takes.")]
    [SerializeField] private float _dayLengthInMinutes = 24f;
    [SerializeField] private Transform _sunLight;

    public float CurrentHour { get; private set; } = 8f; // Start at 8 AM
    public int CurrentDay { get; private set; } = 1;

    public event Action OnDayPassed;
    public event Action<float> OnHourChanged;

    private float _lastHourBroadcast = -1f;

    private void Update()
    {
        Tick(Time.deltaTime);
    }

    public void Tick(float deltaSeconds)
    {
        float timeScale = 24f / (_dayLengthInMinutes * 60f);
        CurrentHour += deltaSeconds * timeScale;

        if (CurrentHour >= 24f)
        {
            CurrentHour -= 24f;
            CurrentDay++;
            OnDayPassed?.Invoke();
        }

        int intHour = Mathf.FloorToInt(CurrentHour);
        if (intHour != _lastHourBroadcast)
        {
            _lastHourBroadcast = intHour;
            OnHourChanged?.Invoke(CurrentHour);
        }

        UpdateSunRotation();
    }

    private void UpdateSunRotation()
    {
        if (_sunLight == null) return;
        
        // 6 AM = 0 degrees (sunrise), 12 PM = 90 degrees (noon), 6 PM = 180 degrees (sunset)
        float sunAngle = (CurrentHour - 6f) / 24f * 360f;
        _sunLight.rotation = Quaternion.Euler(sunAngle, 0f, 0f);
    }

    public void SetTime(float newHour) => CurrentHour = Mathf.Repeat(newHour, 24f);
}
```

## Best Practices
- ✅ Separate the time counting logic from the visual rendering updates.
- ✅ Use events (`OnHourChanged`, `OnDayPassed`) so other systems can react without polling.
- ✅ Scale sun intensity and ambient light based on time of day (using AnimationCurves).
- ❌ **NEVER** use physics or collision to detect time of day; just track the float value.
- ❌ **NEVER** bake lighting in a scene meant for a dynamic Day/Night cycle.

## Related Skills
- `@save-load-serialization` — Save the CurrentDay and CurrentHour.
- `@event-bus-system` — Broadcast time changes globally without tight coupling.
