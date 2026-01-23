---
name: juice-game-feel
description: Implements "Juiciness" effects like Screen Shake, Hit Stop, and Squash & Stretch. Use to "make it feel good", "add impact", or "screen shake".
argument-hint: "name='CameraFeedback' namespace='Game.Feedback'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Juice & Game Feel

## Goal
To add the "polish" that distinguishes a prototype from a product. We implement standard feedback loops.

## Effects
1.  **Screen Shake**: Random displacement of camera.
2.  **Hit Stop**: Freezing time (`Time.timeScale = 0`) for a split second on impact.
3.  **Squash & Stretch**: Scaling geometry on jump/land.

## Procedure
1.  **Generate Controller**: Create `FeedbackController.cs`.
2.  **Instruction**: Attach to Camera (for shake) or Manager.

## Few-Shot Example
User: "Add impact when enemy dies."
Agent: Generates `FeedbackController`. "Call `PlayHitStop()` and `PlayShake()` on death event."
