---
name: menu-navigation-flow
description: Generates a Stack-based Menu Manager. Use to "handle back button", "screen navigation", or "menu popup".
argument-hint: "name='UIManager' namespace='Game.UI'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Menu Navigation & Flow

## Goal
To manage complex UI hierarchies where the user drills down (Main -> Options -> Audio) and needs to return easily.

## Architecture
- **MenuManager**: Holds a `Stack<Menu>`.
- **Menu**: Abstract base class for screens.

## Procedure
1.  **Generate Manager**: `MenuManager.cs`.
2.  **Generate Base**: `Menu.cs`.

## Few-Shot Example
User: "Make a pause menu system."
Agent: Generates `MenuManager`. "Make your PauseScreen inherit from `Menu` and call `manager.OpenMenu(pause)`."
