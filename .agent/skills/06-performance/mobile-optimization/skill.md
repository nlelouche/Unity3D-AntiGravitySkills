---
name: mobile-optimization
description: Sets up Target Frame Rate, VSync, and Resolution Scaling. Use for "Android performance", "limit fps", or "battery saving".
argument-hint: "name='AppConfig' namespace='Game.Core'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Mobile Optimization

## Goal
To ensure the game runs smoothly on devices without draining battery or overheating.

## Architecture
- **AppConfig**: MonoBehaviour running on startup (`[RuntimeInitializeOnLoadMethod]` or Start).

## Procedure
1.  **Generate Config**: `AppConfig.cs`.
2.  **Instruction**: Set TargetFPS to 60 (or 30 for battery saver).

## Few-Shot Example
User: "The game is draining battery."
Agent: Generates `AppConfig` and suggests `TargetFrameRate = 30`.
