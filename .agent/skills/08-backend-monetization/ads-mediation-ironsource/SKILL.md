---
name: ads-mediation-ironsource
description: "Full integration guide for IronSource/LevelPlay mediation: banner, interstitial, and rewarded ads lifecycle, GDPR consent flow, and waterfall configuration."
version: 2.0.0
tags: ["backend", "monetization", "ads", "ironsource", "levelplay", "mediation", "rewarded", "gdpr"]
argument-hint: "ad_type='rewarded|interstitial|banner' action='show|load|setup'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.ironsource.mediation"
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for:
    - "com.ironsource.mediation"
performance_budget:
  gc_alloc_per_frame: "0 bytes (event-driven, no Update polling)"
  max_update_cost: "N/A — event callbacks only"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Ads Mediation — IronSource / LevelPlay

## Overview
**IronSource LevelPlay** (now Unity LevelPlay) is the leading mediation platform, aggregating AdMob, Meta, AppLovin, and others through a single SDK. This skill covers the complete integration: consent flow, SDK initialization, and the three ad unit types (Banner, Interstitial, Rewarded).

## When to Use
- Use for **free-to-play mobile games** monetized via ads.
- Use when targeting multiple ad networks via a single integration.
- Use for **rewarded ads** (watch to earn lives/coins).
- ❌ Do NOT use in paid premium games or PC/console-first titles.

## Ad Unit Lifecycle

```
REWARDED AD LIFECYCLE:
  Initialize → Load → (User triggers) → Show → [Watch] → OnRewarded callback
                ↑                                         |
                └─────────────── Load (pre-cache next) ───┘

INTERSTITIAL:
  Initialize → Load → (Level complete) → Show → OnClosed → Load next

BANNER:
  Initialize → Load+Show → DestroyBanner (scene transition)
```

## Procedure

### 1. Install SDK
```
Unity Package Manager → Add by URL or import .unitypackage from:
https://developers.is.com/ironsource-mobile/unity/unity-plugin/
```

### 2. Initialize + Consent

```csharp
// --- IAdsService.cs ---
using System;
using System.Threading.Tasks;

public interface IAdsService
{
    Task InitializeAsync(string appKey);
    void LoadRewarded();
    bool IsRewardedReady { get; }
    void ShowRewarded(Action<bool> onComplete);
    void ShowInterstitial();
    void ShowBanner();
    void DestroyBanner();
}

// --- IronSourceAdsService.cs ---
using System;
using System.Threading.Tasks;
using UnityEngine;

public class IronSourceAdsService : MonoBehaviour, IAdsService
{
    public bool IsRewardedReady => IronSource.Agent.isRewardedVideoAvailable();

    private Action<bool> _rewardCallback;

    public async Task InitializeAsync(string appKey)
    {
        // GDPR Consent (required in EU)
        var consent = await GetGdprConsentAsync();
        IronSource.Agent.setConsent(consent);
        IronSource.Agent.setMetaData("is_child_directed", "false");

        IronSource.Agent.validateIntegration();
        IronSource.Agent.init(appKey);

        // Register event handlers
        IronSourceRewardedVideoEvents.onAdAvailableEvent        += _ => LoadRewarded();
        IronSourceRewardedVideoEvents.onAdRewardedEvent         += OnRewarded;
        IronSourceRewardedVideoEvents.onAdShowFailedEvent       += OnRewardedFailed;
        IronSourceInterstitialEvents.onAdClosedEvent            += _ => LoadInterstitial();
    }

    public void LoadRewarded()       => IronSource.Agent.loadRewardedVideo();
    private void LoadInterstitial()  => IronSource.Agent.loadInterstitial();

    public void ShowRewarded(Action<bool> onComplete)
    {
        if (!IsRewardedReady) { onComplete?.Invoke(false); return; }
        _rewardCallback = onComplete;
        IronSource.Agent.showRewardedVideo();
    }

    public void ShowInterstitial()
    {
        if (IronSource.Agent.isInterstitialReady())
            IronSource.Agent.showInterstitial();
    }

    public void ShowBanner()
    {
        IronSource.Agent.loadBanner(IronSourceBannerSize.BANNER, IronSourceBannerPosition.BOTTOM);
        IronSource.Agent.displayBanner();
    }

    public void DestroyBanner() => IronSource.Agent.destroyBanner();

    // --- Callbacks ---
    private void OnRewarded(IronSourcePlacement placement, IronSourceAdInfo info)
    {
        _rewardCallback?.Invoke(true);
        _rewardCallback = null;
        LoadRewarded(); // Pre-cache next ad
    }

    private void OnRewardedFailed(IronSourceError error, IronSourceAdInfo info)
    {
        Debug.LogError($"[Ads] Rewarded failed: {error.getDescription()}");
        _rewardCallback?.Invoke(false);
        _rewardCallback = null;
    }

    private async Task<bool> GetGdprConsentAsync()
    {
        // Show your consent dialog and return user choice
        // Integrate with Unity's Data Privacy API or your own UI
        return await Task.FromResult(true); // Replace with real consent dialog
    }

    // Forward Unity lifecycle to IronSource
    private void OnApplicationPause(bool isPaused) => IronSource.Agent.onApplicationPause(isPaused);
}
```

### 3. Usage in Game Code

```csharp
// Reward player for watching ad
public void OnWatchAdButtonClicked()
{
    _adsService.ShowRewarded(rewarded =>
    {
        if (rewarded)
        {
            _playerGold += 50;
            Debug.Log("[Game] Rewarded granted: +50 gold");
        }
        else
        {
            Debug.Log("[Game] Ad not completed — no reward given");
        }
    });
}
```

## GDPR Compliance Checklist

```
☐ Show consent dialog before SDK init in EU regions
☐ setConsent(true/false) based on user choice
☐ setMetaData("is_child_directed", "false") if not COPPA-relevant
☐ Do NOT show personalized ads without explicit consent
☐ Store consent decision in PlayerPrefs across sessions
```

## Best Practices

- ✅ **Pre-cache ads**: Call `LoadRewarded()` at level start, not when the button is pressed.
- ✅ **Validate integration**: Call `IronSource.Agent.validateIntegration()` once during dev.
- ✅ **Handle failure gracefully**: Always check `IsRewardedReady` before showing.
- ✅ Destroy banners on scene transitions to free memory.
- ❌ **NEVER** reward players without a server-side callback for competitive content.
- ❌ **NEVER** call SDK before consent is collected in GDPR regions.
- ❌ **NEVER** show ads during loading screens or gameplay tutorials.



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void AdsMediationIronsource_Should{ExpectedBehavior}_When{Condition}()
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
public void AdsMediationIronsource_ShouldHandle{EdgeCase}()
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
public void AdsMediationIronsource_ShouldThrow_When{InvalidInput}()
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

- `@monetization-iap` — Combine ads + IAP for hybrid monetization
- `@analytics-heatmaps` — Track ad engagement events
- `@service-locator-pattern` — Register `IAdsService` at bootstrap

## Template Files

- `templates/IAdsService.cs.txt` — Interface contract
- `templates/IronSourceAdsService.cs.txt` — Full implementation
- `templates/MockAdsService.cs.txt` — Test mock
