---
name: addressables-asset-management
description: Generates Asset Loading logic. Use to "load prefab asynchronously", "remote content", or "DLC system".
argument-hint: "name='AssetManager' namespace='Game.Core'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Addressables & Asset Management

## Goal
To decouple game logic from hard references, reducing memory usage and startup time.

## Architecture
- **AssetManager**: Wrapper around `Addressables.LoadAssetAsync`.
- **Key**: String or AssetReference.

## Procedure
1.  **Generate Wrapper**: `AssetManager.cs`.
2.  **Instruction**: Mark assets as Addressable in Editor.

## Few-Shot Example
User: "Load the boss enemy only when needed."
Agent: Generates `AssetManager`. "Use `LoadAsset<GameObject>('Boss')` in the trigger."
