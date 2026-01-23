---
name: unity-state-machine-architect
description: Principal Architect for State-Based Logic (FSM/HFSM). Activate this skill when the user requests "enemy AI behaviors," "gameplay flow management," "villager/production cycles," or when refactoring complex if-else blocks.
---

# State Machine Architect (Agentic Production Standard 2.0)

## ?? Context & Goal
[cite_start]The objective is to structure dynamic behaviors through discrete states and controlled transitions. [cite_start]This skill mandates the decomposition of logic into self-contained entities, eliminating "spaghetti code" and allowing the agent to autonomously add new states (e.g., a "Panic" state for villagers) without affecting existing system stability[cite: 8, 237].

## ?? Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating code, the agent MUST perform a logical deconstruction to ensure trust calibration[cite: 27]:
1. [cite_start]**State Identification**: Define the minimum set of required states (e.g., `Idle`, `Search`, `Execute`, `Deliver`)[cite: 239].
2. **Transition Mapping**: Identify the specific triggers (e.g., "target lost," "inventory full") that cause state changes.
3. **Hierarchy Assessment**: Determine if the system requires a Hierarchical State Machine (HFSM) to group shared behaviors and reduce redundancy.
4. **Lifecycle Management**: Plan the cleanup logic for each state to prevent "zombie" processes or memory leaks.

## ??? Operational Procedure (Step-by-Step)
1.  [cite_start]**Artifact Generation (State Transition Map)**: Emit a structured plan or a Mermaid diagram visualizing all states and their transition conditions for human verification before implementation[cite: 32, 64].
2.  **State Abstraction**: Define an `IState` interface or abstract base class with mandatory hooks: `Enter()`, `Update()`, `FixedUpdate()`, and `Exit()`.
3.  **Machine Driver Implementation**: Create the controller component that manages the current state reference and executes transition logic.
4.  **Memory Optimization**: Use the Flyweight pattern to pre-instantiate states during initialization, preventing heap allocations (`new State()`) during gameplay.
5.  **Self-Correction Audit**: Verify the implementation against the "Constraints" section of this skill.

## ?? Constraints & Prohibitions (Hard Rules)
- [cite_start]**FORBIDDEN**: Using massive `switch` statements or `if-else` chains inside a MonoBehaviour's `Update` for complex AI logic[cite: 237].
- [cite_start]**FORBIDDEN**: Changing states by directly manipulating external variables; transitions must be managed exclusively by the State Machine[cite: 8].
- [cite_start]**MANDATORY**: Implement thorough cleanup of events, timers, or UniTasks within the `Exit()` method of every state[cite: 88].
- [cite_start]**MANDATORY**: Use the **Progressive Disclosure** principle¡ªkeep state classes focused only on their specific behavior to minimize context saturation[cite: 41, 46].

## ?? Artifact: State Machine & Transition Audit
The agent must verify the output against this checklist:
- [ ] [cite_start]**Visualization**: Has a transition map been generated for architectural review? [cite: 32]
- [ ] **Encapsulation**: Does each state have a single, clear responsibility?
- [ ] **Decoupling**: Are individual states independent of each other's internal logic?

## ?? Few-Shot Examples
- **User Input**: "Create an enemy that patrols a path but chases the player if they enter a detection radius."
- [cite_start]**Agent Output**: Generates a **State Transition Map** with `Patrol` and `Chase` states, followed by a decoupled FSM implementation where the `Chase` state only knows it must move toward a target[cite: 237].