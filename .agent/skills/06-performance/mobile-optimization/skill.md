---
name: mobile-optimization
description: "Sets up Target Frame Rate, VSync, and Resolution Scaling. Use for "Android performance", "limit fps", or "battery saving"."
version: 1.0.0
tags: []
argument-hint: name='AppConfig' namespace='Game.Core'
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

## When to Use
- Use when mobile optimization
- Use when platform constraints
- Use when battery/thermal

## Architecture
- **AppConfig**: MonoBehaviour running on startup (`[RuntimeInitializeOnLoadMethod]` or Start).

## Procedure
1.  **Generate Config**: `AppConfig.cs`.
2.  **Instruction**: Set TargetFPS to 60 (or 30 for battery saver).

## Few-Shot Example
User: "The game is draining battery."
Agent: Generates `AppConfig` and suggests `TargetFrameRate = 30`.
