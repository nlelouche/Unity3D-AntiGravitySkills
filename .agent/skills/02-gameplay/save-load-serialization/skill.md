---
name: save-load-serialization
description: "Complete save/load system with ISaveable interface, JSON serialization, save slots, and encryption support."
version: 1.0.0
tags: ["gameplay", "save", "load", "serialization", "persistence"]
argument-hint: "action='save' slot=0 OR action='implement_saveable' class='Player'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Save Load Serialization

## Overview
Complete save/load system using ISaveable interface pattern. Automatically discovers saveable objects, serializes to JSON, supports multiple save slots, and optional encryption.

## When to Use
- Use when implementing save game functionality
- Use when persisting player progress
- Use when saving inventory, quests, world state
- Use when implementing cloud saves (with adapter)
- Use when autosave is needed

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SaveManager                             │
│              (Central Controller)                           │
├─────────────────────────────────────────────────────────────┤
│  Save() / Load() / SaveToSlot(n) / LoadFromSlot(n)          │
│  FindAllSaveables() → Collect ISaveable objects             │
│  Serialize to JSON → Write to persistentDataPath            │
└─────────────────────────────────────────────────────────────┘
                              ↓
           ┌──────────────────┼──────────────────┐
           ↓                  ↓                  ↓
   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
   │ PlayerStats   │  │   Inventory   │  │   QuestLog    │
   │ : ISaveable   │  │  : ISaveable  │  │  : ISaveable  │
   └───────────────┘  └───────────────┘  └───────────────┘
         ↓                    ↓                    ↓
   CaptureState()      CaptureState()      CaptureState()
   RestoreState()      RestoreState()      RestoreState()
```

## Components

| Component | Purpose |
|-----------|---------|
| `ISaveable` | Interface for saveable objects |
| `SaveManager` | Central save/load controller |
| `SaveData` | Container for all save states |

## ISaveable Implementation

```csharp
public class PlayerStats : MonoBehaviour, ISaveable
{
    public string SaveId => "player_stats";
    public int LoadPriority => 0; // Load first
    
    [Serializable]
    private struct SaveState
    {
        public int Level;
        public float Experience;
        public int Gold;
    }
    
    public object CaptureState()
    {
        return new SaveState 
        { 
            Level = _level, 
            Experience = _experience,
            Gold = _gold
        };
    }
    
    public void RestoreState(object state)
    {
        var data = (SaveState)state;
        _level = data.Level;
        _experience = data.Experience;
        _gold = data.Gold;
    }
}
```

## Best Practices
- ✅ Use unique SaveId (GUID or hierarchical path)
- ✅ Use LoadPriority for dependencies (Stats before Inventory)
- ✅ Use [Serializable] structs for save state
- ✅ Handle migration for version changes
- ✅ Validate data on load
- ❌ **NEVER** store MonoBehaviour references
- ❌ **NEVER** store ScriptableObject directly (use ID)
- ❌ **NEVER** assume save data exists

## Few-Shot Examples

### Example 1: Save Game
**User**: "Save the game when player presses F5."

**Agent**:
```csharp
if (Input.GetKeyDown(KeyCode.F5))
{
    SaveManager.Instance.Save();
    ShowNotification("Game Saved!");
}
```

### Example 2: Multiple Slots
**User**: "Implement 3 save slots."

**Agent**:
```csharp
public void ShowSaveSlots()
{
    for (int i = 0; i < 3; i++)
    {
        bool hasSave = SaveManager.Instance.HasSave(i);
        // Show slot UI with save info
    }
}
```

### Example 3: Autosave
**User**: "Autosave every 5 minutes."

**Agent**:
```csharp
IEnumerator AutosaveLoop()
{
    while (true)
    {
        yield return new WaitForSeconds(300f);
        SaveManager.Instance.SaveToSlot(99); // Autosave slot
    }
}
```

## Related Skills
- `@inventory-crafting-logic` - Saving inventory
- `@dialogue-quest-system` - Saving quests
- `@advanced-game-bootstrapper` - Load on startup

## Template Files
- `templates/ISaveable.cs.txt` - Interface
- `templates/SaveManager.cs.txt` - Controller
