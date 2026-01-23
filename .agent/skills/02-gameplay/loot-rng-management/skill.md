---
name: loot-rng-management
description: Generates Loot Tables and RNG logic. Use to "create drop system", "random rewards", or "weighted RNG".
argument-hint: "name='ChestLoot' namespace='Game.Loot'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Loot & RNG Management

## Goal
To manage random rewards using a controlled **Weighted System** rather than pure random. This allows designers to balance "Rare" vs "Common" drops easily.

## Architecture
- **DropTable (SO)**: Configurable asset with a list of items and their weights.
- **Logic**: The `GetDrop()` method handles the cumulative probability math.

## Procedure
1.  **Generate Asset**: Create `DropTable.cs`.
2.  **Instruction**: User should create the asset in Unity and assign prefabs.

## Few-Shot Example
User: "Create a loot system for monsters."
Agent: Generates `DropTable.cs`. "Create a DropTable asset for each monster type."
