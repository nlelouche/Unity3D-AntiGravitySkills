---
name: multiplayer-netcode
description: "Setup for Unity Netcode for GameObjects (NGO). Handles connection, synchronization, RPCs, and NetworkVariables."
version: 2.0.0
tags: ["multiplayer", "networking", "ngo", "sync", "rpc"]
argument-hint: "role='Host' OR action='Spawn' prefab='Player'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "N/A - async or editor-only"
  max_update_cost: "N/A"
tdd_first: false
---

# Multiplayer Netcode (NGO)

## Overview
Implementation of Unity Netcode for GameObjects (NGO). Covers connection management (Host/Client), state synchronization (NetworkVariables), messaging (RPCs), and object spawning.

## When to Use
- Use for CO-OP games
- Use for competitive multiplayer
- Use when state needs to be synced
- Use for lobby systems
- Use for authoritative server logic

## Key Concepts

| Concept | Description |
|---------|-------------|
| **NetworkManager** | Core component handling connections |
| **NetworkBehaviour** | MonoBehavior extension for networked scripts |
| **NetworkVariable** | Variables synced automatically |
| **ServerRpc** | Client asks Server to do something |
| **ClientRpc** | Server tells Client to do something |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AUTHORITATIVE SERVER                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   CLIENT A                SERVER (Host)             CLIENT B│
│  ┌──────────────┐        ┌──────────────┐      ┌──────────┐ │
│  │ Input (Move) │───────▶│ Validate     │◀─────│ Input    │ │
│  │              │ Start  │ Update State │      │          │ │
│  │ Present View │◀───────│ Broadcast    │──────▶ Present  │ │
│  └──────────────┘ Server │ State        │      │ View     │ │
│                   RPC    └──────────────┘      └──────────┘ │
│                             ClientRPC                       │
│                         NetworkVariable                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Separate Visuals from Logic
- ✅ Use `NetworkVariable` for state (Health, Ammo)
- ✅ Use RPCs for events (Explosions, Emotes)
- ✅ Validate all ServerRPCs (Anti-cheat)
- ✅ Spawn networked objects via `NetworkObject.Spawn()`
- ❌ **NEVER** sync input directly (sync results/commands)
- ❌ **NEVER** modify NetworkVariables on the client
- ❌ **NEVER** use `Instantiate` for networked objects directly

## Few-Shot Examples

### Example 1: Player Movement (Server Authoritative)
**User**: "Sync player movement."

**Agent**:
```csharp
public class PlayerNet : NetworkBehaviour
{
    public override void OnNetworkSpawn() { ... }

    [ServerRpc]
    public void MoveServerRpc(Vector3 input)
    {
        // Server validates and moves
        transform.position += input * Speed * Time.deltaTime;
    }
    
    void Update() {
        if (IsOwner) {
            MoveServerRpc(Input.GetAxis("Vertical"));
        }
    }
}
```

### Example 2: Synced Variable (Health)
**User**: "Sync health across clients."

**Agent**:
```csharp
public class HealthNet : NetworkBehaviour
{
    public NetworkVariable<int> Health = new NetworkVariable<int>(100);

    public override void OnNetworkSpawn()
    {
        Health.OnValueChanged += (oldVal, newVal) => UpdateHealthBar(newVal);
    }
    
    [ServerRpc]
    public void TakeDamageServerRpc(int amount)
    {
        Health.Value -= amount; // Auto-syncs to all clients
    }
}
```

### Example 3: Spawning Objects
**User**: "Spawn a bullet."

**Agent**:
```csharp
// MUST be run on Server
private void Fire()
{
    var bullet = Instantiate(_bulletPrefab, pos, rot);
    bullet.GetComponent<NetworkObject>().Spawn();
}
```

## Related Skills
- `@backend-integration` - Lobbies and Relay
- `@object-pooling-system` - Networked pooling
- `@asynchronous-programming` - Connection timeouts
