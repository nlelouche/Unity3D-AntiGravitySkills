---
name: multiplayer-netcode
description: Generates Network Manager stubs. Use to "setup multiplayer", "host game", or "client connection".
argument-hint: "name='GameNetworkManager' namespace='Game.Net'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Multiplayer Netcode

## Goal
To provide the entry point for multiplayer logic (NGO/Photon).

## Procedure
1.  **Generate Manager**: `NetworkManager.cs`.
2.  **Instruction**: Ensure the relevant package (com.unity.netcode.gameobjects) is installed.

