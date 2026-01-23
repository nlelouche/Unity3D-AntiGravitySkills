---
name: save-load-serialization
description: Generates a Persistence System (JSON). Use to "save game", "load player data", or "implement checkpoints".
argument-hint: "name='SaveSystem' namespace='Game.Core'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Save & Load Serialization

## Goal
To implement a reliable persistence layer. We default to **JSON** for debuggability but encapsulate it so it can be swapped for Binary/Encrypted flavors.

## Architecture
- **GameData**: A pure C# class (`[Serializable]`) holding the state.
- **SaveManager**: Handles File I/O.
- **ISaveable**: Interface for objects (Player, Chests) to write to `GameData`.

## Procedure
1.  **Generate Data Container**: `GameData.cs`.
2.  **Generate Manager**: `SaveManager.cs`.
3.  **Instruction**: Call `manager.SaveGame()` on checkpoints.

## Few-Shot Example
User: "I need to save the player's level."
Agent: Generates system. "Add `public int Level;` to `GameData.cs` and update it before saving."
