---
name: navmesh-pathfinding
description: "Unity NavMesh integration for AI pathfinding with agents, obstacles, and off-mesh links."
version: 1.0.0
tags: ["gameplay", "AI", "pathfinding", "NavMesh", "movement"]
argument-hint: "agent_type='Humanoid' speed='3.5' angular_speed='120'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# NavMesh Pathfinding

## Overview
Unity NavMesh integration for AI pathfinding. Configure agents, bake navigation meshes, handle obstacles, and create off-mesh links for jumping/climbing.

## When to Use
- Use when AI needs to navigate environments
- Use when enemies chase or patrol
- Use when NPCs need to avoid obstacles
- Use when creating dynamic obstacles
- Use when AI needs to jump gaps or climb

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NavMesh Surface                          │
│              (Baked Navigation Data)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    NavMeshAgent                             │
│              (On AI Entity)                                 │
├─────────────────────────────────────────────────────────────┤
│  SetDestination(target)                                     │
│  Speed, AngularSpeed, StoppingDistance                      │
│  AreaMask, AgentTypeID                                      │
└─────────────────────────────────────────────────────────────┘
              ↕                              ↕
┌─────────────────────┐        ┌─────────────────────┐
│  NavMeshObstacle    │        │   Off-Mesh Link     │
│  (Dynamic Blocker)  │        │   (Jump/Climb)      │
└─────────────────────┘        └─────────────────────┘
```

## Agent Settings
- **Speed**: Movement speed (m/s)
- **Angular Speed**: Rotation speed (deg/s)
- **Acceleration**: Speed change rate
- **Stopping Distance**: How close to destination
- **Auto Braking**: Slow down near destination
- **Obstacle Avoidance**: Quality vs performance

## Area Types
- **Walkable**: Normal ground (cost 1)
- **Not Walkable**: Blocked areas
- **Jump**: Off-mesh link areas
- **Custom**: Water, Road, etc. with cost modifiers

## Best Practices
- ✅ Use NavMesh Surfaces for runtime baking
- ✅ Set appropriate stopping distance
- ✅ Use area costs for path preferences
- ✅ Enable obstacle avoidance for crowds
- ❌ **NEVER** call SetDestination every frame
- ❌ **NEVER** forget to bake after level changes

## Few-Shot Examples

### Example 1: Chase Player
**User**: "Enemy chases player using NavMesh."

**Agent**:
```csharp
NavMeshAgent agent = GetComponent<NavMeshAgent>();
agent.SetDestination(player.transform.position);
```

### Example 2: Patrol Points
**User**: "Guard patrols between waypoints."

**Agent**:
```csharp
if (agent.remainingDistance < 0.5f)
{
    currentWaypoint = (currentWaypoint + 1) % waypoints.Length;
    agent.SetDestination(waypoints[currentWaypoint].position);
}
```

### Example 3: Check Path Valid
**User**: "Only chase if path exists."

**Agent**:
```csharp
NavMeshPath path = new NavMeshPath();
if (NavMesh.CalculatePath(start, end, NavMesh.AllAreas, path))
{
    if (path.status == NavMeshPathStatus.PathComplete)
        agent.SetPath(path);
}
```

## Related Skills
- `@ai-behavior-trees` - AI decision making
- `@physics-logic` - Collision handling
- `@advanced-character-controller` - Player movement

## Template Files
Available in templates/ folder.
