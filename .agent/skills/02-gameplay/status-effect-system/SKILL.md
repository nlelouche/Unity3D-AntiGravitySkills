---
name: status-effect-system
description: Generates a Buff/Debuff system. Use to "add poison", "healing over time", "slow effect", or "stat modifiers".
argument-hint: "name='StatusManager' namespace='Game.Combat'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Status Effect System

## Goal
To manage temporal modifications to an entity (Poison, Haste, Shield).

## Architecture
- **EffectData (SO)**: Static definition (Duration, Icon).
- **ActiveEffect (Class)**: Runtime instance tracking `RemainingTime`.
- **EffectManager**: The engine that ticks and expires effects.

## Procedure
1.  **Generate Data**: `EffectData.cs`.
2.  **Generate Manager**: `EffectManager.cs`.

## Few-Shot Example
User: "Make a poison potion."
Agent: Generates system. "Create an `EffectData` asset named 'Poison', set `HasTick=true`, `TickAmount=5`."
