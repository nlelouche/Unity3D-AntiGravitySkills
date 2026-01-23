---
name: inventory-crafting-logic
description: Generates an MVC-based Inventory System. Use to "create inventory", "implement crafting", or "item database".
argument-hint: "name='PlayerInventory' namespace='Game.Inventory'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Inventory & Crafting Logic

## Goal
To provide a scalable Inventory System using **MVC (Model-View-Controller)**. This allows the same inventory logic to be used for Players, Chests, and NPCs without rewriting UI code.

## Architecture
- **Model (Pure C#)**: `InventoryModel`. Handles stacks, capacity, and events (`OnUpdated`).
- **Data (SO)**: `ItemData`. definitions.
- **Controller (MonoBehaviour)**: `InventoryController`. Links the Model to the View.

## Procedure
1.  **Generate Data Definition**: `ItemData.cs`.
2.  **Generate Logic**: `InventoryModel.cs` (UnitTestable).
3.  **Generate Bridge**: `InventoryController.cs`.

## Few-Shot Example
User: "Make a backpack system."
Agent: Generates `BackpackModel` (Logic) and `BackpackController` (Unity Component).
