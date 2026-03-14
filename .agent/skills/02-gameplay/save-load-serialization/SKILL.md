---
name: save-load-serialization
description: "Complete save/load system with ISaveable interface, JSON serialization, save slots, and encryption support."
version: 2.0.0
tags: ["gameplay", "save", "load", "serialization", "persistence"]
argument-hint: "action='save' slot=0 OR action='implement_saveable' class='Player'"
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
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
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



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void SaveLoadSerialization_Should{ExpectedBehavior}_When{Condition}()
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
public void SaveLoadSerialization_ShouldHandle{EdgeCase}()
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
public void SaveLoadSerialization_ShouldThrow_When{InvalidInput}()
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
- `@inventory-crafting-logic` - Saving inventory
- `@dialogue-quest-system` - Saving quests
- `@advanced-game-bootstrapper` - Load on startup

## Template Files
- `templates/ISaveable.cs.txt` - Interface
- `templates/SaveManager.cs.txt` - Controller
