---
name: mobile-optimization
description: "Mobile-specific optimization for Android/iOS including framerate, resolution, thermal, and battery management."
version: 1.0.0
tags: ["performance", "mobile", "Android", "iOS", "battery"]
argument-hint: "fps='60' OR quality='medium' thermal='true'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Mobile Optimization

## Overview
Mobile-specific performance optimization for Android/iOS. Covers framerate targeting, resolution scaling, thermal throttling, and battery efficiency.

## When to Use
- Use for Android/iOS builds
- Use when battery drain is high
- Use when device overheats
- Use for adaptive quality
- Use for low-end device support

## Mobile Constraints

```
┌─────────────────────────────────────────────────────────────┐
│                 MOBILE PERFORMANCE PYRAMID                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌────────┐                               │
│                    │ BATTERY│                               │
│                    └────┬───┘                               │
│                ┌────────┴────────┐                          │
│                │    THERMAL      │                          │
│                └────────┬────────┘                          │
│           ┌─────────────┴─────────────┐                     │
│           │         MEMORY            │                     │
│           └─────────────┬─────────────┘                     │
│      ┌──────────────────┴──────────────────┐                │
│      │             CPU / GPU               │                │
│      └─────────────────────────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Settings

| Setting | Low Device | High Device |
|---------|:----------:|:-----------:|
| Target FPS | 30 | 60 |
| Resolution Scale | 0.7 | 1.0 |
| Shadow Resolution | 512 | 2048 |
| Texture Quality | Half | Full |
| MSAA | Off | 2x |

## Optimization Techniques

| Technique | Impact | Implementation |
|-----------|:------:|----------------|
| Frame Rate Cap | High | Application.targetFrameRate |
| Resolution Scale | High | Screen.SetResolution |
| VSync | Medium | QualitySettings.vSyncCount |
| GPU Skinning | Medium | Player Settings |
| Texture Streaming | High | QualitySettings |

## Best Practices
- ✅ Profile on actual device
- ✅ Use Adaptive Performance (Samsung)
- ✅ Implement quality presets
- ✅ Reduce draw calls (<100)
- ✅ Use texture atlases
- ❌ **NEVER** target 60fps on low-end
- ❌ **NEVER** ignore thermal throttling
- ❌ **NEVER** use max quality by default

## Few-Shot Examples

### Example 1: App Configuration
**User**: "Set up mobile performance."

**Agent**:
```csharp
public class MobileConfig : MonoBehaviour
{
    [Header("Performance")]
    [SerializeField] private int _targetFPS = 60;
    [SerializeField] private bool _enableVSync = true;
    [SerializeField] private float _resolutionScale = 1f;
    
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    private static void Initialize()
    {
        var config = new MobileConfig();
        config.ApplySettings();
    }
    
    public void ApplySettings()
    {
        Application.targetFrameRate = _targetFPS;
        QualitySettings.vSyncCount = _enableVSync ? 1 : 0;
        
        if (_resolutionScale < 1f)
        {
            int width = (int)(Screen.width * _resolutionScale);
            int height = (int)(Screen.height * _resolutionScale);
            Screen.SetResolution(width, height, true);
        }
    }
}
```

### Example 2: Adaptive Quality
**User**: "Auto-adjust quality based on FPS."

**Agent**:
```csharp
public class AdaptiveQuality : MonoBehaviour
{
    [SerializeField] private int _targetFPS = 30;
    [SerializeField] private int _fpsThresholdLow = 25;
    [SerializeField] private int _fpsThresholdHigh = 40;
    
    private float _checkInterval = 5f;
    private float _timer;
    private float _avgFPS;
    
    private void Update()
    {
        _avgFPS = Mathf.Lerp(_avgFPS, 1f / Time.deltaTime, 0.1f);
        _timer += Time.deltaTime;
        
        if (_timer >= _checkInterval)
        {
            AdjustQuality();
            _timer = 0;
        }
    }
    
    private void AdjustQuality()
    {
        int current = QualitySettings.GetQualityLevel();
        
        if (_avgFPS < _fpsThresholdLow && current > 0)
        {
            QualitySettings.DecreaseLevel();
            Debug.Log("Quality decreased");
        }
        else if (_avgFPS > _fpsThresholdHigh && current < QualitySettings.names.Length - 1)
        {
            QualitySettings.IncreaseLevel();
            Debug.Log("Quality increased");
        }
    }
}
```

### Example 3: Battery Saver Mode
**User**: "Add battery saving option."

**Agent**:
```csharp
public void EnableBatterySaver(bool enabled)
{
    if (enabled)
    {
        Application.targetFrameRate = 30;
        QualitySettings.SetQualityLevel(0); // Lowest
        Screen.brightness = 0.5f;
    }
    else
    {
        Application.targetFrameRate = 60;
        QualitySettings.SetQualityLevel(2); // Medium
        Screen.brightness = 1f;
    }
    
    PlayerPrefs.SetInt("BatterySaver", enabled ? 1 : 0);
}
```

## Platform Specifics
- **Android**: Use Adaptive Performance SDK
- **iOS**: Check thermalState notifications
- **Both**: Test on min-spec devices

## Related Skills
- `@object-pooling-system` - GC-free spawning
- `@lod-occlusion-culling` - Rendering optimization
- `@memory-profiler-expert` - Memory limits
