---
name: advanced-game-bootstrapper
description: "Implements the Bootstrap Scene pattern. Guarantees deterministic initialization of global systems before gameplay starts."
version: 1.0.0
tags: ["architecture", "bootstrap", "initialization", "managers", "singleton-alternative"]
argument-hint: "name='GameBootstrapper' namespace='Game.Core'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Advanced Game Bootstrapper

## Overview
Eliminate "Singleton Hell" and race conditions during game startup. The game MUST start from a specialized Bootstrap scene that loads all Managers (Sound, Save, Network) in deterministic order before showing any UI or Gameplay.

## When to Use
- Use when starting a new Unity project
- Use when experiencing race conditions between managers
- Use when "Manager X not ready" errors occur on scene load
- Use when replacing scattered static singletons with proper architecture
- Use when implementing async initialization (loading screens)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BUILD INDEX 0                            │
│                   BOOTSTRAP SCENE                           │
├─────────────────────────────────────────────────────────────┤
│  GameBootstrapper (DontDestroyOnLoad)                       │
│    ├── AudioManager (order: 0)                              │
│    ├── SaveManager (order: 5)                               │
│    ├── NetworkManager (order: 10)                           │
│    └── AnalyticsManager (order: 15)                         │
├─────────────────────────────────────────────────────────────┤
│  [Optional] Loading Screen UI                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   MAIN MENU SCENE
                          ↓
                   GAMEPLAY SCENE
```

## Components

| Component | Purpose |
|-----------|---------|
| `IInitializable` | Interface for async initialization with ordering |
| `IShutdownable` | Interface for clean shutdown on quit |
| `GameBootstrapper` | Orchestrates initialization sequence |
| `BaseManager` | Abstract base for all global managers |

## Procedure
1. **Create Bootstrap Scene**: New scene, set as Build Index 0
2. **Generate Components**: Create `IInitializable.cs`, `GameBootstrapper.cs`, `BaseManager.cs`
3. **Create Managers**: Inherit from `BaseManager` for each system
4. **Configure Order**: Set `InitializationOrder` (0-10: core, 11-50: gameplay, 51+: UI)
5. **Assign References**: Drag managers to GameBootstrapper in inspector

## Best Practices
- ✅ Always use `async/await` for initialization that may take time
- ✅ Implement `IShutdownable` for managers that need cleanup
- ✅ Use `InitializationOrder` to enforce dependencies
- ✅ Keep Bootstrap scene as lightweight as possible
- ✅ Show loading progress to users during initialization
- ❌ **NEVER** use `Awake`/`Start` for cross-manager dependencies
- ❌ **NEVER** use static singletons (use DI or service locator instead)
- ❌ **NEVER** skip the bootstrap scene in builds

## Testing Protocol
| Mode | Approach |
|------|----------|
| **Production** | Always start from Bootstrap scene |
| **Editor (Scene)** | Create `EditorBootstrap` prefab with mocked managers |
| **Unit Tests** | Mock `IInitializable` implementations |

## Few-Shot Examples

### Example 1: Race Condition Fix
**User**: "The game crashes because AudioManager isn't ready when Player spawns."

**Agent**:
```
1. Implement Bootstrap Scene pattern
2. Create AudioManager : BaseManager with order 0
3. Create PlayerSpawner that only runs after bootstrap complete
4. AudioManager guaranteed ready before any gameplay
```

### Example 2: Loading Screen Integration
**User**: "I want a loading bar while systems initialize."

**Agent**:
```
1. Add loading UI prefab to Bootstrap scene
2. Connect to GameBootstrapper._progressBar and _statusText
3. Progress updates automatically during initialization
```

### Example 3: Network + Save Dependencies
**User**: "SaveManager needs NetworkManager to be ready first."

**Agent**:
```
1. NetworkManager.InitializationOrder = 5
2. SaveManager.InitializationOrder = 10
3. Bootstrapper initializes in order: Network → Save
```

## Related Skills
- `@di-container-manager` - For injecting bootstrapped managers
- `@event-bus-system` - For broadcasting initialization events
- `@scriptableobject-architecture` - For configuration data

## Template Files
- `templates/IInitializable.cs.txt` - Core interface
- `templates/GameBootstrapper.cs.txt` - Main bootstrapper
- `templates/BaseManager.cs.txt` - Manager base class
