---
name: advanced-game-bootstrapper
description: Implements the "Bootstrap Scene" pattern. Guarantees deterministic initialization of global systems before gameplay starts.
argument-hint: "name='GameBootstrapper' namespace='Game.Core'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Advanced Game Bootstrapper

## Goal
To eliminate "Singleton Hell" and "Race Conditions" during game start. The game MUST start from a specialized `Bootstrap` scene that loads all Managers (`Sound`, `Save`, `Network`) before showing any UI or Gameplay.

## Architecture
- **Bootstrap Scene**: Scene index 0. Contains ONLY the `Bootstrapper` and Global Managers.
- **IInitializable**: Interface for async setup (`await Initialize()`).
- **Scene Flow**: `Bootstrap` -> (Init) -> `MainMenu` -> `Gameplay`.

## Testing Protocol
- **Production**: Start from `Bootstrap` scene.
- **Unit Testing**: Create a `TestBootstrap` prefab that mocks the managers, drop it into your Test Scene. This decouples the "Bootstrap Logic" from the "Scene Asset".

## Procedure
1.  **Generate Core**: `IInitializable.cs` and `Bootstrapper.cs`.
2.  **Instruction**: 
    - Create a scene named "Bootstrap".
    - Add `Bootstrapper` component.
    - Assign your Global Managers (Audio, Save) to it.
    - Ensure Managers are `DontDestroyOnLoad` (or let Bootstrapper handle it).

## Few-Shot Example
User: "The game crashes because AudioManager isn't ready when Player spawns."
Agent: "I will implement the **Bootstrap Pattern**. The AudioManager will be initialized and marked 'Ready' in the Bootstrap scene *before* the Player scene is ever loaded."
