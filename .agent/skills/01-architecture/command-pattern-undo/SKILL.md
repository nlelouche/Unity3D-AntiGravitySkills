---
name: command-pattern-undo
description: "Implements the Command Pattern with a full undo/redo history stack. Applicable to editor tools, strategy game moves, crafting systems, or any operation that must be reversible."
version: 2.0.0
tags: ["architecture", "command-pattern", "undo-redo", "editor-tools", "strategy", "SOLID"]
argument-hint: "action='generate' name='BuildingPlacementCommand' OR action='wire-undo-redo'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: false
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes (commands execute on demand, not per-frame)"
  max_update_cost: "O(1) — stack push/pop"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Command Pattern + Undo/Redo

## Overview
The **Command Pattern** encapsulates an operation as an object, decoupling the **invoker** (button, hotkey) from the **receiver** (game state). When combined with a history **stack**, you get full undo/redo. Use it for custom editor tools (Ctrl+Z), strategy game moves ("take back"), level designers, or any gameplay system requiring reversible operations.

## When to Use
- Use for **custom Unity Editor tools** that modify scene data.
- Use for **strategy/puzzle gameplay** where moves must be undoable.
- Use for **crafting/inventory operations** that can be cancelled.
- Use for **level editors** inside your game (e.g. base-building).
- ❌ Do NOT use for real-time continuous actions (movement each frame) — too much state capture overhead.

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                  COMMAND PATTERN + HISTORY                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  INVOKER                    HISTORY STACK                     │
│  ┌────────────────┐         ┌───────────────────────────┐    │
│  │ UI Button      │─Execute─▶ CommandHistory             │    │
│  │ Hotkey Handler │         │  Stack<ICommand> _undo    │    │
│  │ AI Decision    │◀─Undo───│  Stack<ICommand> _redo    │    │
│  └────────────────┘         └───────────────────────────┘    │
│                                        │                      │
│                           ┌────────────▼───────────────┐     │
│                           │        ICommand             │     │
│                           │  Execute()                  │     │
│                           │  Undo()                     │     │
│                           └────────────────────────────┘     │
│                                        │                      │
│              ┌─────────────────────────┼──────────────────┐  │
│              ▼                         ▼                   ▼  │
│   ┌───────────────────┐  ┌───────────────────┐  ┌──────────┐│
│   │PlaceBuildingCommand│  │DestroyUnitCommand │  │MoveCmd  ││
│   └───────────────────┘  └───────────────────┘  └──────────┘│
└───────────────────────────────────────────────────────────────┘
```

## TDD Contract

```csharp
[Test]
public void Command_Execute_AppliesStateChange()
{
    var inventory = new Inventory();
    var cmd = new AddItemCommand(inventory, new Item("Sword"));

    cmd.Execute();

    Assert.AreEqual(1, inventory.ItemCount);
}

[Test]
public void Command_Undo_RevertsStateChange()
{
    var inventory = new Inventory();
    var cmd = new AddItemCommand(inventory, new Item("Sword"));

    cmd.Execute();
    cmd.Undo();

    Assert.AreEqual(0, inventory.ItemCount);
}

[Test]
public void CommandHistory_Undo_RestoresPreviousState()
{
    var history = new CommandHistory();
    var inventory = new Inventory();

    history.Execute(new AddItemCommand(inventory, new Item("Shield")));
    history.Undo();

    Assert.AreEqual(0, inventory.ItemCount);
}
```

## Core Implementation

```csharp
// --- ICommand.cs ---
public interface ICommand
{
    void Execute();
    void Undo();
}

// --- CommandHistory.cs ---
using System.Collections.Generic;

public class CommandHistory
{
    private readonly Stack<ICommand> _undoStack = new();
    private readonly Stack<ICommand> _redoStack = new();

    public void Execute(ICommand command)
    {
        command.Execute();
        _undoStack.Push(command);
        _redoStack.Clear(); // New command clears redo history
    }

    public void Undo()
    {
        if (_undoStack.Count == 0) return;
        var command = _undoStack.Pop();
        command.Undo();
        _redoStack.Push(command);
    }

    public void Redo()
    {
        if (_redoStack.Count == 0) return;
        var command = _redoStack.Pop();
        command.Execute();
        _undoStack.Push(command);
    }

    public bool CanUndo => _undoStack.Count > 0;
    public bool CanRedo => _redoStack.Count > 0;
}

// --- Example: PlaceBuildingCommand.cs ---
public class PlaceBuildingCommand : ICommand
{
    private readonly BuildingGrid _grid;
    private readonly Vector2Int   _cell;
    private readonly BuildingType _type;
    private GameObject            _instance;

    public PlaceBuildingCommand(BuildingGrid grid, Vector2Int cell, BuildingType type)
    {
        _grid = grid;
        _cell = cell;
        _type = type;
    }

    public void Execute()
    {
        _instance = _grid.PlaceBuilding(_cell, _type);
    }

    public void Undo()
    {
        _grid.RemoveBuilding(_cell);
        Object.Destroy(_instance);
        _instance = null;
    }
}
```

## Wiring in MonoBehaviour

```csharp
public class LevelEditorController : MonoBehaviour
{
    private readonly CommandHistory _history = new();

    private void Update()
    {
        // Ctrl+Z / Ctrl+Y
        if (Input.GetKeyDown(KeyCode.Z) && (Input.GetKey(KeyCode.LeftControl) || Input.GetKey(KeyCode.LeftCommand)))
            _history.Undo();

        if (Input.GetKeyDown(KeyCode.Y) && (Input.GetKey(KeyCode.LeftControl) || Input.GetKey(KeyCode.LeftCommand)))
            _history.Redo();
    }

    public void OnPlaceBuilding(Vector2Int cell, BuildingType type)
    {
        _history.Execute(new PlaceBuildingCommand(_buildingGrid, cell, type));
    }
}
```

## Best Practices

- ✅ Each command must be **self-contained** — capture all state needed to undo at construction time.
- ✅ Clear `_redoStack` when a new command is executed (prevents branching history).
- ✅ Set a **max history size** for memory-constrained platforms.
- ✅ For Unity Editor tools, combine with `Undo.RecordObject()` to integrate with the native Undo system.
- ❌ **NEVER** store scene references that can become null — use IDs and look them up in `Execute()`/`Undo()`.
- ❌ **NEVER** use for continuous per-frame operations — only discrete actions.

## Related Skills

- `@custom-editor-scripting` — Integrate with Unity's native `Undo.RecordObject`
- `@grid-based-building-system` — Primary use case consumer
- `@save-load-serialization` — Serialize command history for save/resume
