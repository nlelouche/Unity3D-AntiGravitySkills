---
name: state-machine-architect
description: "Generates a flexible State Machine system for player controllers, AI, or any state-based logic. Supports hierarchical states and transitions."
version: 1.0.0
tags: ["architecture", "state-machine", "FSM", "player-controller", "AI"]
argument-hint: "name='PlayerController' namespace='Game.Player' states='Idle,Walk,Run,Jump'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# State Machine Architect

## Overview
Generate flexible, modular state machines for player controllers, AI, UI systems, or any state-based logic. Uses the State Pattern with generic typing for maximum reusability.

## When to Use
- Use when implementing player character states (Idle, Walk, Run, Jump)
- Use when creating AI behavior states (Patrol, Chase, Attack, Flee)
- Use when managing UI screen flow (MainMenu, Settings, Gameplay)
- Use when game states need clear boundaries (Playing, Paused, GameOver)
- Use instead of complex if/else or switch statements

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    StateMachine<TContext>                   │
├─────────────────────────────────────────────────────────────┤
│  AddState<TState>(state)                                    │
│  ChangeState<TState>()                                      │
│  Update() / FixedUpdate()                                   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │  IdleState  │ │  WalkState  │ │  JumpState  │
      │ : IState<T> │ │ : IState<T> │ │ : IState<T> │
      └─────────────┘ └─────────────┘ └─────────────┘
```

## Components

| Component | Purpose |
|-----------|---------|
| `IState<TContext>` | Interface for all states |
| `StateMachine<TContext>` | Manages state instances and transitions |
| `StateBase<TContext>` | Abstract base class with boilerplate |

## Procedure
1. **Define Context**: The owner object (usually MonoBehaviour)
2. **Create States**: Implement `IState<TContext>` or inherit `StateBase<TContext>`
3. **Initialize Machine**: Create `StateMachine<TContext>` with context
4. **Register States**: Call `AddState<T>(new TState())` for each
5. **Set Initial State**: Call `ChangeState<TInitialState>()`
6. **Update Loop**: Call `machine.Update()` in MonoBehaviour.Update()

## Best Practices
- ✅ Use the Context object to access shared data
- ✅ Keep states focused (Single Responsibility)
- ✅ Use `OnStateChanged` event for debugging/logging
- ✅ Consider state history for "return to previous state"
- ✅ Use `StateBase<T>` for cleaner code
- ❌ **NEVER** put transition logic outside states
- ❌ **NEVER** use strings for state identification (use types)
- ❌ **NEVER** access private MonoBehaviour members directly

## Few-Shot Examples

### Example 1: Player Controller
**User**: "Create a state machine for player movement with Idle, Walk, Run, Jump."

**Agent**:
```csharp
// Context is the PlayerController MonoBehaviour
public class IdleState : StateBase<PlayerController>
{
    public override void Enter(PlayerController ctx)
    {
        ctx.Animator.Play("Idle");
    }
    
    public override void Update(PlayerController ctx)
    {
        if (ctx.Input.MoveVector.magnitude > 0.1f)
            TransitionTo<WalkState>();
        if (ctx.Input.JumpPressed)
            TransitionTo<JumpState>();
    }
}

// In PlayerController.cs
private StateMachine<PlayerController> _stateMachine;

void Start()
{
    _stateMachine = new StateMachine<PlayerController>(this);
    _stateMachine.AddState(new IdleState());
    _stateMachine.AddState(new WalkState());
    _stateMachine.AddState(new JumpState());
    _stateMachine.ChangeState<IdleState>();
}

void Update() => _stateMachine.Update();
void FixedUpdate() => _stateMachine.FixedUpdate();
```

### Example 2: AI Enemy
**User**: "Create enemy AI with Patrol, Chase, Attack states."

**Agent**:
```csharp
public class PatrolState : StateBase<EnemyAI>
{
    public override void Update(EnemyAI ctx)
    {
        ctx.MoveToNextWaypoint();
        if (ctx.CanSeePlayer)
            TransitionTo<ChaseState>();
    }
}
```

### Example 3: Game Flow
**User**: "State machine for MainMenu, Playing, Paused, GameOver."

**Agent**:
```csharp
// GameManager as context
// States control Time.timeScale, UI visibility, etc.
```

## Related Skills
- `@advanced-design-patterns` - State pattern fundamentals
- `@ai-behavior-trees` - More complex AI decision making
- `@advanced-character-controller` - Uses state machine internally

## Template Files
- `templates/IState.cs.txt` - Core state interface
- `templates/StateMachine.cs.txt` - Generic state machine
- `templates/StateBase.cs.txt` - Abstract state base class