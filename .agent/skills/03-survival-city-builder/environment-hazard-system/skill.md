---
name: environment-hazard-system
description: Generates Survival Stats (Hunger/Thirst) and Environmental Factors (Temp). Use to "add survival mechanics", "weather damage", or "hunger system".
argument-hint: "name='SurvivalStats' namespace='Game.Survival'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Environment Hazard System

## Goal
To implement the "Tick" based survival loop (e.g., Hunger -1 every second).

## Architecture
- **SurvivalManager**: Handles the Tick timer.
- **Stat**: Class with Value, Max, and DecayRate.

## Procedure
1.  **Generate System**: `SurvivalManager.cs`.

## Few-Shot Example
User: "Add hunger and thirst."
Agent: Generates `SurvivalManager` with customizable Decay Stats.
