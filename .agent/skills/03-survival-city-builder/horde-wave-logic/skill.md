---
name: horde-wave-logic
description: "Generates a Wave Spawner system. Use to "create enemy waves", "tower defense spawning", or "horde mode"."
version: 1.0.0
tags: []
argument-hint: name='WaveSpawner' namespace='Game.Combat'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Horde & Wave Logic

## Goal
To manage spawning of enemies in waves, typical of Tower Defense or Survival modes.

## When to Use
- Use when wave-based spawning
- Use when enemy waves
- Use when horde survival mechanics

## Architecture
- **WaveConfig (SO)**: Defines *what* and *how many* to spawn.
- **WaveManager**: Coroutine-based spawner that iterates through the config.

## Procedure
1.  **Generate Data**: `WaveConfig.cs`.
2.  **Generate Logic**: `WaveManager.cs`.

## Few-Shot Example
User: "Make an enemy spawner."
Agent: Generates system. "Create a WaveConfig asset, add zombies to it, and assign it to the Spawner."
