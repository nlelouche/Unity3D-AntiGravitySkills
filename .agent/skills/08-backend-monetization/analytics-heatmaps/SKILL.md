---
name: analytics-heatmaps
description: "Implementation of comprehensive analytics tracking and heatmap data collection for player behavior analysis."
version: 2.0.0
tags: ["analytics", "tracking", "heatmaps", "metrics", "telemetry"]
argument-hint: "event='LevelComplete' params='time,score' OR heatmap='death_pos'"
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
  gc_alloc_per_frame: "N/A - async or editor-only"
  max_update_cost: "N/A"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
---

# Analytics & Heatmaps

## Overview
System for tracking player behavior events and spatial data (heatmaps). Supports multiple providers (Unity Analytics, Firebase, Mixpanel) via an interface abstraction.

## When to Use
- Use for measuring retention (Day 1, Day 7)
- Use for balancing game difficulty (win/loss rates)
- Use for finding level design flaws (spatial heatmaps)
- Use for tracking monetization conversion
- Use for debugging user flows (funnels)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ANALYTICS PIPELINE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GAMEPLAY CODE                                              │
│  ┌──────────────────────┐                                   │
│  │ "LevelComplete"      │                                   │
│  │ Params: {Score: 100} │                                   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│             ▼                                               │
│  ANALYTICS MANAGER (Interface)                              │
│  ┌──────────┬───────────┬───────────┐                       │
│  │ Provider │ Provider  │ Heatmap   │                       │
│  │ (Unity)  │ (Google)  │ Recorder  │                       │
│  └──────────┴───────────┴─────┬─────┘                       │
│                               │                             │
│                               ▼                             │
│                         ┌───────────┐                       │
│                         │ LOCAL LOG │ (Dev builds)          │
│                         └───────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## tracked Event Structure

| Event Name | Parameters | Goal |
|------------|------------|------|
| `game_start` | `version`, `platform` | Daily Active Users (DAU) |
| `level_start` | `level_id`, `difficulty` | Engagement |
| `level_complete` | `level_id`, `time`, `score` | Progression |
| `process_fail` | `level_id`, `reason` | Churn analysis |
| `iap_transaction` | `product_id`, `price` | Revenue |

## Best Practices
- ✅ Wrap external SDKs (don't call `Firebase` directly)
- ✅ Use standardized event naming (`noun_verb` or `snake_case`)
- ✅ Track "First Time User Experience" (FTUE) rigidly
- ✅ Record screen resolution and device specs
- ✅ Batch events to save battery
- ❌ **NEVER** track Personally Identifiable Information (PII) without consent
- ❌ **NEVER** track high-frequency events (e.g., Update loop)
- ❌ **NEVER** rely on client-side timestamps (use server time)

## Few-Shot Examples

### Example 1: Analytics Service
**User**: "Track level completion."

**Agent**:
```csharp
public class AnalyticsService : MonoBehaviour
{
    public void TrackLevelComplete(string levelId, int score, float duration)
    {
        var params = new Dictionary<string, object>
        {
            { "level_id", levelId },
            { "score", score },
            { "duration_seconds", duration },
            { "user_level", _player.Level }
        };
        
        SendEvent("level_complete", params);
    }
    
    private void SendEvent(string name, Dictionary<string, object> parameters)
    {
        // Wrapper for SDKs
        Unity.Services.Analytics.AnalyticsService.Instance.CustomData(name, parameters);
        Debug.Log($"[Analytics] {name}: {JsonConvert.SerializeObject(parameters)}");
    }
}
```

### Example 2: Heatmap Recorder
**User**: "Record where players die."

**Agent**:
```csharp
public class HeatmapRecorder : MonoBehaviour
{
    public void RecordDeath(Vector3 position)
    {
        // Round to grid to save data density
        int x = Mathf.RoundToInt(position.x);
        int z = Mathf.RoundToInt(position.z);
        
        var data = new Dictionary<string, object>
        {
            { "pos_x", x },
            { "pos_z", z },
            { "level", SceneManager.GetActiveScene().name }
        };
        
        AnalyticsService.Instance.TrackEvent("player_death_location", data);
    }
}
```

### Example 3: Funnel Tracking
**User**: "Track tutorial steps."

**Agent**:
```csharp
public void TrackTutorialStep(int stepIndex, string stepName)
{
    AnalyticsService.Instance.TrackEvent("tutorial_step", new() {
        { "step_index", stepIndex },
        { "step_name", stepName },
        { "time_since_start", Time.timeSinceLevelLoad }
    });
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
public void AnalyticsHeatmaps_Should{ExpectedBehavior}_When{Condition}()
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
public void AnalyticsHeatmaps_ShouldHandle{EdgeCase}()
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
public void AnalyticsHeatmaps_ShouldThrow_When{InvalidInput}()
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
- `@backend-integration` - Store analytics remotely
- `@monetization-iap` - Track purchases
- `@mobile-optimization` - Battery-safe tracking
