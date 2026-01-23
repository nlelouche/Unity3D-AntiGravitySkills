---
name: ui-toolkit-architect
description: Generates UI Toolkit assets (UXML, USS) and C# Controllers following MVVM. Use when creating "menus", "HUDs", or "interface panels".
argument-hint: "panel_name='MainMenu' namespace='Game.UI'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# UI Toolkit Architect

## Goal
To create modern, scalable user interfaces using Unity's **UI Toolkit**. We strictly separate structure (UXML), style (USS), and logic (C# Controller/ViewModel).

## Architecture: MVVM (Model-View-ViewModel)
- **View (UXML/USS)**: The layout and look.
- **Controller (MonoBehaviour)**: Binds the View elements to the ViewModel events.
- **ViewModel (Pure C#)**: Holds the state (e.g., `Score`, `Health`) and Commands.

## Procedure
1.  **Generate Assets**: Create `{Name}.uxml` and `{Name}.uss` in `Assets/UI/{Name}/`.
2.  **Generate Logic**: Create `{Name}Controller.cs` attached to a `UIDocument`.
3.  **Link**: Ensure the Controller knows how to find the buttons defined in UXML (Query by name).

## Few-Shot Example
User: "Create a Pause Menu."
Agent:
1.  Creates `PauseMenu.uxml` with "Resume" and "Quit" buttons.
2.  Creates `PauseMenu.uss` with styling.
3.  Creates `PauseMenuController.cs` that binds `root.Q<Button>("Resume")` to `Time.timeScale = 1`.
