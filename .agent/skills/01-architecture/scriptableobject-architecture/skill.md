---
name: scriptableobject-architecture
description: "Senior Architect for Data-Driven Design using ScriptableObjects. Create SO-based event channels, runtime sets, and configuration data."
version: 1.0.0
tags: ["architecture", "scriptableobject", "data-driven", "events", "configuration"]
argument-hint: "type='event' name='OnPlayerDamaged' OR type='data' name='WeaponConfig'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# ScriptableObject Architecture

## Overview
Decouple gameplay data and signals from MonoBehaviour logic using ScriptableObjects as the "Single Source of Truth" for design constants and event broadcasting.

## When to Use
- Use when creating inspector-configurable game data (stats, costs, timings)
- Use when implementing SO-based event channels (alternative to static EventBus)
- Use when tracking active objects without GameObject.Find (Runtime Sets)
- Use when sharing data between scenes or objects
- Use when designers need to tweak values without code changes

## Architecture

### Data-Driven Configuration
```
┌─────────────────────────────────────────────────────────────┐
│                    ScriptableObject Asset                   │
│                     (WeaponConfigSO)                        │
├─────────────────────────────────────────────────────────────┤
│  [SerializeField] private float _damage = 10f;              │
│  [SerializeField] private float _fireRate = 0.5f;           │
│  [SerializeField] private GameObject _projectilePrefab;     │
│                                                             │
│  public float Damage => _damage;                            │
│  public float FireRate => _fireRate;                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
      Shared by multiple weapons without duplication
```

### Event Channels
```
┌──────────────┐           ┌──────────────────┐
│   Trigger    │  Raise()  │   GameEventSO    │
│ (Door opens) │ ─────────→│ (OnDoorOpened)   │
└──────────────┘           └────────┬─────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ↓                     ↓                     ↓
      ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
      │  AudioManager │    │  UI Manager   │    │  Quest System │
      │  (Listener)   │    │  (Listener)   │    │  (Listener)   │
      └───────────────┘    └───────────────┘    └───────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| `GameEventSO` | SO-based event for inspector-assignable broadcasts |
| `GameEventListener` | MonoBehaviour that listens to GameEventSO |
| `RuntimeSetSO<T>` | Dynamic collection of active objects |
| `ConfigSO` | Base for configuration data containers |

## Best Practices
- ✅ Use `[SerializeField] private` with public getters
- ✅ Include validation attributes (`[Range]`, `[Min]`)
- ✅ Use `[CreateAssetMenu]` with hierarchical paths
- ✅ Reset runtime data in `OnDisable` for editor play mode
- ✅ Keep SO as data containers, NOT execution logic
- ❌ **NEVER** put Update loops in ScriptableObjects
- ❌ **NEVER** store direct MonoBehaviour references in persistent SOs
- ❌ **NEVER** use heavy assets (textures) directly (use AssetReference)

## Few-Shot Examples

### Example 1: Weapon Configuration
**User**: "Create configurable weapon stats for the RPG."

**Agent**:
```csharp
[CreateAssetMenu(menuName = "Game/Combat/WeaponConfig")]
public class WeaponConfigSO : ScriptableObject
{
    [Header("Damage")]
    [SerializeField, Min(1)] private float _baseDamage = 10f;
    [SerializeField] private DamageType _damageType;
    
    [Header("Timing")]
    [SerializeField, Range(0.1f, 2f)] private float _attackSpeed = 1f;
    
    public float BaseDamage => _baseDamage;
    public DamageType DamageType => _damageType;
    public float AttackSpeed => _attackSpeed;
}
```

### Example 2: SO Event Channel
**User**: "Door should play sound and update UI without coupling."

**Agent**:
```csharp
// 1. Create GameEventSO asset "OnDoorOpened"
// 2. Door.cs calls: _onDoorOpenedEvent.Raise();
// 3. AudioManager has GameEventListener pointing to same SO
// 4. UI has another GameEventListener pointing to same SO
```

### Example 3: Runtime Set
**User**: "Track all active enemies for wave completion check."

**Agent**:
```csharp
[CreateAssetMenu(menuName = "Game/Runtime/EnemySet")]
public class EnemyRuntimeSetSO : RuntimeSetSO<Enemy> { }

// Enemy.cs
void OnEnable() => _enemySet.Add(this);
void OnDisable() => _enemySet.Remove(this);

// WaveManager.cs
bool IsWaveComplete => _enemySet.Count == 0;
```

## Related Skills
- `@event-bus-system` - Static alternative to SO events
- `@advanced-design-patterns` - Patterns using SO data
- `@di-container-manager` - Injecting SO dependencies

## Template Files
- `templates/GameEventSO.cs.txt` - Event channel
- `templates/GameEventListener.cs.txt` - Event listener
- `templates/RuntimeSetSO.cs.txt` - Active object tracking