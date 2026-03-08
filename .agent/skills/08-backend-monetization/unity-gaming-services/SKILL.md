---
name: unity-gaming-services
description: "Complete setup guide for Unity Gaming Services (UGS): Authentication, Lobby, Relay, Leaderboards, Cloud Save. First-party backend for Unity 6 multiplayer and live-ops projects."
version: 2.0.0
tags: ["backend", "ugs", "lobby", "relay", "authentication", "leaderboards", "cloud-save", "multiplayer"]
argument-hint: "service='auth|lobby|relay|leaderboards|cloud-save' action='setup|implement'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.unity.services.core"
    - "com.unity.services.authentication"
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for:
    - "com.unity.services.core"
    - "com.unity.services.authentication"
    - "com.unity.services.lobby"
    - "com.unity.services.relay"
performance_budget:
  gc_alloc_per_frame: "N/A — async network calls only"
  max_update_cost: "N/A — event-driven"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Unity Gaming Services (UGS)

## Overview
Unity Gaming Services is the **first-party backend suite** for Unity 6 games. It provides Authentication, Lobby, Relay (NAT traversal), Leaderboards, Cloud Save, and Cloud Code — all integrated into the Unity Dashboard and Package Manager. The recommended backend for new Unity-native multiplayer and live-ops projects.

## When to Use
- Use for **multiplayer sessions** (Lobby + Relay + NGO).
- Use for **cloud-saved player progress** across devices.
- Use for **global leaderboards** without a custom server.
- ❌ Do NOT use if your game is fully offline with no cloud features.

## Service Map

| Service | Purpose | Required Package |
|---------|---------|-----------------|
| **Authentication** | Anonymous + platform login | `com.unity.services.authentication` |
| **Lobby** | Room creation & match discovery | `com.unity.services.lobby` |
| **Relay** | Peer-to-peer NAT traversal | `com.unity.services.relay` |
| **Leaderboards** | Score ranking | `com.unity.services.leaderboards` |
| **Cloud Save** | Cross-device persistence | `com.unity.services.cloudsave` |

## Setup Checklist

```
☐ 1. Create project at dashboard.unity3d.com
☐ 2. Link: Edit → Project Settings → Services → Link
☐ 3. Install packages (Package Manager → Add by name):
      com.unity.services.core
      com.unity.services.authentication
      (+ service-specific packages above)
☐ 4. Implement InitializeAsync() at game boot (see below)
```

## Core Implementation

```csharp
// --- IUGSAuthService.cs ---
using System.Threading.Tasks;

public interface IUGSAuthService
{
    Task   InitializeAsync();
    Task   SignInAnonymouslyAsync();
    string PlayerId  { get; }
    bool   IsSignedIn { get; }
}

// --- UGSAuthService.cs ---
using System.Threading.Tasks;
using Unity.Services.Authentication;
using Unity.Services.Core;
using UnityEngine;

public class UGSAuthService : IUGSAuthService
{
    public string PlayerId   => AuthenticationService.Instance.PlayerId;
    public bool   IsSignedIn => AuthenticationService.Instance.IsSignedIn;

    public async Task InitializeAsync()
    {
        if (UnityServices.State == ServicesInitializationState.Initialized) return;
        await UnityServices.InitializeAsync();
    }

    public async Task SignInAnonymouslyAsync()
    {
        if (IsSignedIn) return;
        try   { await AuthenticationService.Instance.SignInAnonymouslyAsync(); }
        catch (AuthenticationException ex) { Debug.LogError($"[UGS] Auth failed: {ex.Message}"); throw; }
    }
}
```

## Lobby: Create & Join

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Unity.Services.Lobbies;
using Unity.Services.Lobbies.Models;

public class UGSLobbyService
{
    private Lobby _currentLobby;

    public async Task<Lobby> CreateLobbyAsync(string name, int maxPlayers)
    {
        var options = new CreateLobbyOptions { IsPrivate = false };
        _currentLobby = await LobbyService.Instance.CreateLobbyAsync(name, maxPlayers, options);
        return _currentLobby;
    }

    public async Task<Lobby> JoinByCodeAsync(string code) =>
        _currentLobby = await LobbyService.Instance.JoinLobbyByCodeAsync(code);

    // Call every 15s from host to prevent lobby expiry
    public async Task HeartbeatAsync()
    {
        if (_currentLobby != null)
            await LobbyService.Instance.SendHeartbeatPingAsync(_currentLobby.Id);
    }
}
```

## Cloud Save: Player Data

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Unity.Services.CloudSave;

public class UGSCloudSaveService
{
    public async Task SaveAsync<T>(string key, T data)
    {
        await CloudSaveService.Instance.Data.Player.SaveAsync(
            new Dictionary<string, object> { { key, data } });
    }

    public async Task<T> LoadAsync<T>(string key, T defaultValue = default)
    {
        var result = await CloudSaveService.Instance.Data.Player
            .LoadAsync(new HashSet<string> { key });
        return result.TryGetValue(key, out var item) ? item.Value.GetAs<T>() : defaultValue;
    }
}
```

## TDD Contract

```csharp
public class MockUGSAuthService : IUGSAuthService
{
    public string PlayerId   => "mock-player-id";
    public bool   IsSignedIn => true;
    public Task InitializeAsync()       => Task.CompletedTask;
    public Task SignInAnonymouslyAsync() => Task.CompletedTask;
}

[Test]
public async Task Auth_WhenSignedIn_PlayerIdNotEmpty()
{
    var auth = new MockUGSAuthService();
    await auth.SignInAnonymouslyAsync();
    Assert.IsFalse(string.IsNullOrEmpty(auth.PlayerId));
}
```

## Best Practices

- ✅ Always call `InitializeAsync()` + `SignInAnonymouslyAsync()` before any UGS service.
- ✅ Use `IUGSAuthService` interface everywhere — easy mock swap for TDD.
- ✅ Send **Lobby heartbeat** every 15s from the host.
- ✅ Prefer **Cloud Save** over PlayerPrefs for cross-device data.
- ❌ **NEVER** call UGS APIs before initialization completes.
- ❌ **NEVER** submit competitive scores client-side without Cloud Code validation.

## Related Skills

- `@multiplayer-netcode` — NGO + Relay for the transport layer
- `@playfab-economy-v2` — Alternative backend for economy and virtual currency
- `@repository-pattern` — Wrap Cloud Save behind `IRepository<T>`
- `@service-locator-pattern` — Register `IUGSAuthService` at bootstrap
