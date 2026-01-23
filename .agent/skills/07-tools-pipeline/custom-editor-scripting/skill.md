---
name: custom-editor-scripting
description: Generates Editor Windows and Inspectors. Use to "create tools", "improver pipeline", or "debug window".
argument-hint: "name='MapGenerator' namespace='Game.Editor'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Custom Editor Scripting

## Goal
To accelerate development by building custom tools inside Unity.

## Architecture
- **EditorWindow**: Floating windows (`MenuItem`).
- **CustomEditor**: Modifies the Inspector for a Component.

## Procedure
1.  **Generate Window**: `EditorWindow.cs`.
2.  **Instruction**: Access via "Tools/WindowName".

## Few-Shot Example
User: "Make a tool to rename all enemies."
Agent: Generates `RenamerWindow.cs`.
