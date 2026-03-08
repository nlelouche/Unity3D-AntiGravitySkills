---
name: repository-pattern
description: "Implements the Repository Pattern to decouple game data access from business logic. Provides a generic IRepository<T> with sync and async variants, and mock implementations for TDD."
version: 2.0.0
tags: ["architecture", "repository", "data-access", "decoupling", "SOLID", "TDD", "persistence"]
argument-hint: "action='generate' entity='PlayerSave' backend='LocalJson|PlayFab|PlayerPrefs'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: false
  check_render_pipeline: false
  scan_manifest_for:
    - "com.playfab.unitysdk"
    - "com.unity.services.core"
performance_budget:
  gc_alloc_per_frame: "0 bytes (data ops are async, off hot path)"
  max_update_cost: "N/A — async I/O operations"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Repository Pattern

## Overview
The **Repository Pattern** creates an abstraction layer between the domain logic (what your game does) and the data source (where it stores data). A `PlayerController` asks `IPlayerRepository.LoadAsync()` and doesn't know — or care — whether data comes from PlayerPrefs, JSON files, PlayFab, or a mock in a unit test. This makes game systems **testable, swappable, and backend-agnostic**.

## When to Use
- Use when you need to **save/load** player data, inventory, settings, or scores.
- Use when you want to **swap backends** later (e.g., local JSON → cloud save → PlayFab).
- Use when you want **TDD** for systems that depend on persisted data.
- ❌ Do NOT use for ephemeral in-memory data that doesn't persist across sessions.
- ❌ Do NOT use as a wrapper for simple `PlayerPrefs.GetInt()` calls — overkill.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    REPOSITORY PATTERN                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  DOMAIN LAYER            DATA LAYER                          │
│  ┌───────────────┐       ┌──────────────────────────────┐   │
│  │ GameManager   │       │ IPlayerRepository            │   │
│  │               │──────▶│  LoadAsync(): PlayerData     │   │
│  │ PlayerService │       │  SaveAsync(PlayerData)       │   │
│  └───────────────┘       │  DeleteAsync()               │   │
│                           └──────────────────────────────┘   │
│                                    │ Implemented by          │
│                  ┌─────────────────┼──────────────────┐     │
│                  ▼                 ▼                   ▼     │
│          ┌──────────────┐ ┌─────────────┐ ┌─────────────┐  │
│          │JsonRepository│ │PlayFabRepo  │ │MockRepository│  │
│          │(local files) │ │(cloud save) │ │(unit tests) │  │
│          └──────────────┘ └─────────────┘ └─────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## TDD Contract

```csharp
[Test]
public async Task PlayerRepository_WhenSaved_LoadReturnsCorrectData()
{
    // Arrange — use in-memory mock, no file I/O
    var repo = new InMemoryPlayerRepository();
    var data = new PlayerData { Level = 5, Gold = 1200 };

    // Act
    await repo.SaveAsync(data);
    var loaded = await repo.LoadAsync();

    // Assert
    Assert.AreEqual(5,    loaded.Level);
    Assert.AreEqual(1200, loaded.Gold);
}

[Test]
public async Task PlayerRepository_WhenEmpty_LoadReturnsDefault()
{
    var repo = new InMemoryPlayerRepository();
    var loaded = await repo.LoadAsync();
    Assert.IsNotNull(loaded);
    Assert.AreEqual(1, loaded.Level); // default level
}
```

## Procedure

1.  **Define Entity**: Create a plain C# data class (no MonoBehaviour).
2.  **Define Interface**: Create `IRepository<T>` with async CRUD methods.
3.  **Implement Concrete Repos**: One per backend (JSON, PlayerPrefs, PlayFab).
4.  **Create Mock Repo**: `InMemoryRepository<T>` for unit tests.
5.  **Register**: Use `ServiceLocator` or DI container to inject the concrete repo.

## Core Implementation

```csharp
// --- IRepository.cs ---
using System.Threading.Tasks;

public interface IRepository<T> where T : class, new()
{
    Task<T>    LoadAsync();
    Task       SaveAsync(T data);
    Task       DeleteAsync();
    Task<bool> ExistsAsync();
}

// --- PlayerData.cs (Entity) ---
[System.Serializable]
public class PlayerData
{
    public int    Level     = 1;
    public int    Gold      = 0;
    public string PlayerName = "Hero";
}

// --- JsonPlayerRepository.cs (Local JSON) ---
using System.IO;
using System.Threading.Tasks;
using UnityEngine;
using Newtonsoft.Json; // or JsonUtility

public class JsonPlayerRepository : IRepository<PlayerData>
{
    private readonly string _filePath;

    public JsonPlayerRepository()
    {
        _filePath = Path.Combine(Application.persistentDataPath, "player.json");
    }

    public async Task<PlayerData> LoadAsync()
    {
        if (!File.Exists(_filePath)) return new PlayerData();
        var json = await File.ReadAllTextAsync(_filePath);
        return JsonUtility.FromJson<PlayerData>(json) ?? new PlayerData();
    }

    public async Task SaveAsync(PlayerData data)
    {
        var json = JsonUtility.ToJson(data, prettyPrint: true);
        await File.WriteAllTextAsync(_filePath, json);
    }

    public Task DeleteAsync()
    {
        if (File.Exists(_filePath)) File.Delete(_filePath);
        return Task.CompletedTask;
    }

    public Task<bool> ExistsAsync() => Task.FromResult(File.Exists(_filePath));
}

// --- InMemoryPlayerRepository.cs (for TDD) ---
public class InMemoryPlayerRepository : IRepository<PlayerData>
{
    private PlayerData _store;
    public Task<PlayerData> LoadAsync()          => Task.FromResult(_store ?? new PlayerData());
    public Task            SaveAsync(PlayerData d){ _store = d; return Task.CompletedTask; }
    public Task            DeleteAsync()          { _store = null; return Task.CompletedTask; }
    public Task<bool>      ExistsAsync()          => Task.FromResult(_store != null);
}
```

## Best Practices

- ✅ Always code against `IRepository<T>` — never the concrete class.
- ✅ Create one `InMemoryRepository<T>` implementation for all unit tests.
- ✅ Handle `LoadAsync()` returning null gracefully — return `new T()` as default.
- ✅ Use `async/await` throughout — never block the main thread on file I/O.
- ❌ **NEVER** reference `MonoBehaviour` or `UnityEngine` APIs in a Repository class.
- ❌ **NEVER** call Save/Load from `Update()` — use explicit triggers (save button, scene transition).

## Related Skills

- `@save-load-serialization` — Encryption, versioning, migration for save data
- `@service-locator-pattern` — Register/resolve `IRepository<T>` at bootstrap
- `@backend-integration` — Swap JSON repo for PlayFab or Firebase backend
- `@automated-unit-testing` — Use `InMemoryRepository` for NUnit tests
