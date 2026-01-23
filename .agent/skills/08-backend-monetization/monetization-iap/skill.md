---
name: monetization-iap
description: "Generates IAP Manager stubs. Use to "add in-app purchase", "buy gold", or "setup shop"."
version: 1.0.0
tags: []
argument-hint: name='IAPManager' namespace='Game.IAP'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Monetization & IAP

## Goal
To wrap Unity's IAP system in a simpler Manager.

## When to Use
- Use when in-app purchases
- Use when monetization
- Use when store integration

## Procedure
1.  **Generate Manager**: `IAPManager.cs`.
2.  **Instruction**: Install Unity Purchasing package via Services.

