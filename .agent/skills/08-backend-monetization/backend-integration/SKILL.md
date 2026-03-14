---
name: backend-integration
description: "Integration with Backend-as-a-Service (BaaS) platforms like PlayFab, Firebase, or custom APIs for cloud save, auth, and leaderboards."
version: 2.0.0
tags: ["backend", "playfab", "firebase", "api", "cloud-save", "auth"]
argument-hint: "service='PlayFab' action='Login' OR feature='CloudData'"
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

# Backend Integration

## Overview
Integration strategies for cloud backends. Focuses on PlayFab and Firebase for authentication, cloud data storage, leaderboards, and server-side logic (Cloud Script).

## When to Use
- Use for user accounts (Login/Register)
- Use for cross-device save games
- Use for global leaderboards
- Use for virtual currency and economy
- Use for live events and news

## Common Services

| Feature | PlayFab | Firebase |
|---------|---------|----------|
| **Auth** | LoginWithCustomID | Auth.SignIn |
| **Database** | PlayerData (KV) | Firestore / Realtime DB |
| **Functions** | Azure Functions | Cloud Functions |
| **Storage** | CDN / Content | Storage Buckets |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CLIENT (UNITY)           API GATEWAY (REST)                │
│  ┌──────────────┐        ┌──────────────────┐               │
│  │ Auth Token   │───────▶│ Validate Token   │               │
│  │ Request Data │        │ Route Request    │               │
│  └──────────────┘        └────────┬─────────┘               │
│                                   │                         │
│                                   ▼                         │
│                         ┌───────────────────┐               │
│                         │ SERVERLESS LOGIC  │               │
│                         │ (Validate Rules)  │               │
│                         └─────────┬─────────┘               │
│                                   │                         │
│                                   ▼                         │
│                         ┌───────────────────┐               │
│                         │     DATABASE      │               │
│                         │   (Persistence)   │               │
│                         └───────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Authenticate silently (Auto-login) first
- ✅ Use Cloud Script for sensitive logic (Currency, XP)
- ✅ Cache data locally to avoid API throttling
- ✅ Handle "No Internet" states gracefully
- ✅ Secure API keys (don't commit to Git)
- ❌ **NEVER** trust the client with economy changes
- ❌ **NEVER** store passwords in plain text
- ❌ **NEVER** block the main thread with API calls

## Few-Shot Examples

### Example 1: PlayFab Login
**User**: "Login player silently."

**Agent**:
```csharp
public void Login()
{
    var request = new LoginWithCustomIDRequest
    {
        CustomId = SystemInfo.deviceUniqueIdentifier,
        CreateAccount = true
    };
    
    PlayFabClientAPI.LoginWithCustomID(request, 
        result => Debug.Log("Login Success"), 
        error => Debug.LogError(error.GenerateErrorReport()));
}
```

### Example 2: Update Cloud Data
**User**: "Save player level to cloud."

**Agent**:
```csharp
public void SaveLevel(int level)
{
    var request = new UpdateUserDataRequest
    {
        Data = new Dictionary<string, string> {
            { "PlayerLevel", level.ToString() }
        }
    };
    
    PlayFabClientAPI.UpdateUserData(request, 
        result => Debug.Log("Saved"), 
        error => Debug.LogError("Save Failed"));
}
```

### Example 3: Cloud Script (Economy)
**User**: "Add gold securely."

**Agent**:
```javascript
// Server-side (Azure Function / CloudScript)
handlers.grantGold = function(args, context) {
    var amount = 100; // Fixed server-side
    server.AddUserVirtualCurrency({
        PlayFabId: currentPlayerId,
        VirtualCurrency: "GD",
        Amount: amount
    });
    return { granted: amount };
};
```



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void BackendIntegration_Should{ExpectedBehavior}_When{Condition}()
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
public void BackendIntegration_ShouldHandle{EdgeCase}()
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
public void BackendIntegration_ShouldThrow_When{InvalidInput}()
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
- `@analytics-heatmaps` - Track backend events
- `@monetization-iap` - Validate receipts on backend
- `@asynchronous-programming` - Handle API calls
