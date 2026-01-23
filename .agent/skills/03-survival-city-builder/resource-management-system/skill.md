---
name: resource-management-system
description: Generates an Economy/Resource system. Use for "wood/stone counter", "wallet system", or "crafting cost check".
argument-hint: "name='EconomyManager' namespace='Game.Economy'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Resource Management System

## Goal
To manage integer values associated with ScriptableObject keys (Resources), typical in RTS/Survival games.

## Architecture
- **ResourceType (SO)**: The key (Gold, Wood).
- **ResourceManager (MonoBehaviour)**: The logic (`Dictionary<ResourceType, int>`).
- **Events**: `OnResourceChanged` for UI updates.

## Procedure
1.  **Generate Data**: `ResourceType.cs`.
2.  **Generate Logic**: `ResourceManager.cs`.

## Few-Shot Example
User: "I need to track gold and gems."
Agent: Generates system. "Create two assets: 'Gold' and 'Gems'. Use `manager.AddResource(gold, 100)`."
