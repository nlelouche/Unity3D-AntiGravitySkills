---
name: oop-patterns-architect
description: Generates standard OOP design patterns (State, Command, Observer) for game logic. Use to "create a state machine", "implement command pattern", or "manage game states".
argument-hint: "pattern='state-machine' name='PlayerLocomotion'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# OOP Patterns Architect

## Goal
To implement robust, standard Design Patterns in the Management/OOP Layer of the application. This ensures game logic is decoupled and testable, avoiding "Mega-Classes" with 5000 lines of `switch` statements.

## Pattern 1: The State Machine (HFSM)
Used for Character Controllers, Game Flow, and UI Navigation.
- **Context**: The `MonoBehaviour` (`Controller`) that holds data and references.
- **State**: Abstract class defining `Enter`, `Exit`, `Update`.
- **Concrete States**: Classes like `IdleState`, `JumpState`.

## Procedure
1.  **Analyze Intent**: If the user asks for "Character Logic" or "Game Loop", suggest the State Pattern.
2.  **Generate Core**: Create the `StateBase` and `Controller` from templates.
3.  **Generate States**: specific concrete states requested (e.g., Idle, Walk, Run).

## Few-Shot Example
User: "Create a state machine for EnemyAI."
Agent:
1.  Generates `EnemyAIState.cs` (Abstract).
2.  Generates `EnemyAIController.cs` (Context).
3.  Generates `EnemyAIIdleState.cs` (Concrete).
