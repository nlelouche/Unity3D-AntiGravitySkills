---
name: object-pooling-system
description: "Generates Object Pools to reuse GameObjects (bullets, enemies) and avoid GC spikes."
version: 1.0.0
tags: []
argument-hint: name='BulletPool' namespace='Game.Performance'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Object Pooling System

## Goal
To recycle objects instead of Destroy/Instantiate, crucial for mobile and console performance.

## When to Use
- Use when object pooling
- Use when spawn optimization
- Use when memory efficiency

## Architecture
- **PoolManager**: Holds a `Queue<GameObject>`.
- **IPoolable**: Interface for objects reset logic (`OnSpawn`, `OnDespawn`).

## Procedure
1.  **Generate Manager**: `PoolManager.cs`.
2.  **Instruction**: Assign the prefab in Inspector.

## Few-Shot Example
User: "The game stutters when shooting."
Agent: "I'll implement an Object Pool for the bullets."
