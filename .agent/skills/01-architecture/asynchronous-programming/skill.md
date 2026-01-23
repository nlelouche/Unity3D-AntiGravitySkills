---
name: asynchronous-programming
description: "Master async/await patterns in Unity. Handle loading, network requests, and non-blocking operations correctly."
version: 1.0.0
tags: ["architecture", "async", "await", "Task", "coroutines", "UniTask"]
argument-hint: "operation='LoadScene' OR task='NetworkRequest'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Asynchronous Programming

## Overview
Handle long-running operations (loading, network, file I/O) without blocking the main thread. Master async/await patterns adapted for Unity's unique lifecycle.

## When to Use
- Use when loading assets or scenes
- Use when making network/web requests
- Use when performing file I/O
- Use when waiting for user input with timeouts
- Use when orchestrating sequential async operations

## Async Options in Unity

| Approach | Best For | Unity Integration |
|----------|----------|-------------------|
| **Coroutines** | Simple delays, legacy code | Native `yield return` |
| **async/await (Task)** | C# standard, complex flows | Requires care with main thread |
| **UniTask** | Zero-allocation, Unity-optimized | Recommended for production |

## Key Patterns

### Pattern 1: Coroutines (Legacy)
```csharp
IEnumerator LoadLevel()
{
    _loadingScreen.SetActive(true);
    
    yield return new WaitForSeconds(0.5f);
    
    var operation = SceneManager.LoadSceneAsync("Level1");
    while (!operation.isDone)
    {
        _progressBar.value = operation.progress;
        yield return null;
    }
}
```

### Pattern 2: async/await with Task
```csharp
async Task LoadLevelAsync()
{
    _loadingScreen.SetActive(true);
    
    await Task.Delay(500);
    
    var operation = SceneManager.LoadSceneAsync("Level1");
    while (!operation.isDone)
    {
        _progressBar.value = operation.progress;
        await Task.Yield();
    }
}
```

### Pattern 3: UniTask (Recommended)
```csharp
async UniTaskVoid LoadLevelAsync()
{
    _loadingScreen.SetActive(true);
    
    await UniTask.Delay(500);
    
    await SceneManager.LoadSceneAsync("Level1").ToUniTask(
        Progress.Create<float>(p => _progressBar.value = p)
    );
}
```

## Best Practices
- ✅ Use `CancellationToken` for cancellable operations
- ✅ Handle exceptions with try/catch in async methods
- ✅ Use `async void` ONLY for event handlers (prefer `async UniTaskVoid`)
- ✅ Check `destroyCancellationToken` for MonoBehaviour lifetime
- ✅ Consider UniTask for zero-allocation async
- ❌ **NEVER** use `Task.Run` for Unity API calls (not thread-safe!)
- ❌ **NEVER** forget to await async calls (fire-and-forget = silent errors)
- ❌ **NEVER** block with `.Result` or `.Wait()` (causes deadlock)

## Cancellation Pattern
```csharp
private CancellationTokenSource _cts;

async void Start()
{
    _cts = new CancellationTokenSource();
    
    try
    {
        await LoadDataAsync(_cts.Token);
    }
    catch (OperationCanceledException)
    {
        Debug.Log("Operation cancelled");
    }
}

void OnDestroy()
{
    _cts?.Cancel();
    _cts?.Dispose();
}

async Task LoadDataAsync(CancellationToken token)
{
    token.ThrowIfCancellationRequested();
    // ... async work
}
```

## Coroutine vs Async Comparison

| Feature | Coroutine | async/await |
|---------|-----------|-------------|
| Return values | No | Yes |
| Exception handling | Limited | Full try/catch |
| Cancellation | Manual flags | CancellationToken |
| Composition | Difficult | Easy (await chain) |
| Unit testing | Hard | Easy |
| Allocations | WaitForSeconds allocates | Task allocates (UniTask = zero) |

## Few-Shot Examples

### Example 1: Sequential Loading
**User**: "Load player data, then inventory, then spawn player."

**Agent**:
```csharp
async UniTaskVoid InitializeGame()
{
    var playerData = await LoadPlayerDataAsync();
    var inventory = await LoadInventoryAsync(playerData.Id);
    await SpawnPlayerAsync(playerData, inventory);
    
    Debug.Log("Game initialized!");
}
```

### Example 2: Parallel Loading
**User**: "Load multiple assets simultaneously."

**Agent**:
```csharp
async UniTask LoadAllAssets()
{
    var (textures, sounds, prefabs) = await UniTask.WhenAll(
        LoadTexturesAsync(),
        LoadSoundsAsync(),
        LoadPrefabsAsync()
    );
}
```

### Example 3: Timeout Pattern
**User**: "Network request with 5 second timeout."

**Agent**:
```csharp
async UniTask<string> FetchWithTimeout(string url)
{
    var cts = new CancellationTokenSource();
    cts.CancelAfter(TimeSpan.FromSeconds(5));
    
    try
    {
        return await FetchDataAsync(url, cts.Token);
    }
    catch (OperationCanceledException)
    {
        return "Request timed out";
    }
}
```

## Unity Main Thread Safety
```csharp
// BAD: Called from background thread
Task.Run(() => 
{
    transform.position = Vector3.zero; // CRASH!
});

// GOOD: Return to main thread
await UniTask.SwitchToMainThread();
transform.position = Vector3.zero; // Safe
```

## Related Skills
- `@advanced-game-bootstrapper` - Async initialization
- `@addressables-asset-management` - Async asset loading
- `@multiplayer-netcode` - Async network operations

## Recommended Package
```
UniTask - https://github.com/Cysharp/UniTask
```
Zero-allocation async/await for Unity with full lifecycle integration.