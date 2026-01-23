---
name: input-system-new
description: Setup wrapper for Unity's New Input System. Use to "handle controls", "gamepad support", or "player input".
argument-hint: "name='GameInputReader' namespace='Game.Input'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# New Input System Wrapper

## Goal
To abstract the Input System into a `ScriptableObject` Event Bus. This allows the PlayerController to listen to `OnJump` without knowing if it came from Keyboard or Gamepad.

## Architecture
- **InputReader (SO)**: Implements the generated interface (`IPlayerActions`). Fires C# events.
- **GameInput (Generated)**: Unity's auto-generated C# class from `.inputactions`.

## Procedure
1.  **Generate Reader**: `InputReader.cs`.
2.  **Instruction**: User must click "Generate C# Class" on their `.inputactions` asset first.

## Few-Shot Example
User: "Controls for my character."
Agent: Generates `InputReader.cs`. "Assign this asset to your PlayerController."
