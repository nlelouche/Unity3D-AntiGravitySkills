---
name: advanced-character-controller
description: Generates robust 2D/3D Character Controllers (Kinematic or Rigidbody). Use when user asks for "player movement", "FPS controller", or "platformer physics".
argument-hint: "type='kinematic-3d' name='PlayerController' namespace='Game.Player'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Advanced Character Controller

## Goal
To implement a production-ready Character Controller that feels responsive. We avoid `transform.Translate` in favor of robust physics-based or kinematic solutions.

## Architecture Choices
1.  **Kinematic (`CharacterController`)**:
    - **Pros**: Handles slopes, stairs, and step offsets automatically. No jitter.
    - **Cons**: Doesn't push rigidbodies naturally.
    - **Use Case**: FPS, TPS, Standard Adventure Games.
2.  **Rigidbody (Force-Based)**:
    - **Pros**: Full physics interaction. Can be pushed/pulled.
    - **Cons**: Slippery slopes require custom friction logic. Harder to tune.
    - **Use Case**: Physics Puzzlers, Rocket Jumping, Rolling Balls.

## Procedure
1.  **Analyze Intent**: Ask if the game relies on heavy physics interaction (RB) or precise movement (Kinematic).
2.  **Select Template**:
    - If Kinematic 3D -> `templates/KinematicController3D.cs.txt`
    - If Rigidbody 3D -> `templates/RigidbodyController3D.cs.txt`
3.  **Generate**: Replace placeholders and write to `Assets/Scripts/Player/`.

## Few-Shot Example
**User**: "I need a controller for a shooter game."
**Agent**: "For a shooter, precise movement is key. I will generate a Kinematic Character Controller."
1.  Reads `KinematicController3D.cs.txt`.
2.  Writes `PlayerController.cs`.
