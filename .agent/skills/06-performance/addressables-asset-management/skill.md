---
name: addressables-asset-management
description: "Generates Asset Loading logic. Use to "load prefab asynchronously", "remote content", or "DLC system"."
version: 1.0.0
tags: []
argument-hint: name='AssetManager' namespace='Game.Core'
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

## When to Use
- Use when handling asynchronous operations
- Use when implementing async/await patterns
- Use when managing coroutines vs Tasks
- Use when asset management
- Use when content loading

## Architecture
- **AssetManager**: Wrapper around `Addressables.LoadAssetAsync`.
- **Key**: String or AssetReference.

## Procedure
1.  **Generate Wrapper**: `AssetManager.cs`.
2.  **Instruction**: Mark assets as Addressable in Editor.

## Few-Shot Example
User: "Load the boss enemy only when needed."
Agent: Generates `AssetManager`. "Use `LoadAsset<GameObject>('Boss')` in the trigger."
