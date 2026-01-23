---
name: ai-behavior-trees
description: Generates a Node-Based Behavior Tree system (Selector, Sequence, Action). Use to "create enemy AI", "patrol logic", or "NPC decision making".
argument-hint: "name='EnemyBT' namespace='Game.AI'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# AI Behavior Trees

## Goal
To implement a modular AI system using **Behavior Trees**. This is superior to State Machines for complex decision making because it allows hierarchical composition (Sequences, Selectors).

## Architecture
- **Node**: Abstract base.
- **Composite**: Holds list of Nodes (`Selector`, `Sequence`).
- **Leaf (Action)**: Performs actual logic (`MoveTo`, `Attack`).

## Procedure
1.  **Generate Core**: Create `Node.cs`, `Selector.cs`, `Sequence.cs`.
2.  **Generate Tree**: Create a main `Tree` MonoBehaviour that instantiates the root node.
3.  **Generate Actions**: Create example actions like `TaskPatrol`, `TaskAttack`.

## Few-Shot Example
User: "Make an AI that patrols and attacks."
Agent:
1.  Generates Core Nodes.
2.  Creates `GuardTree.cs`.
3.  Constructs: `root = new Selector(new List<Node> { new Sequence(Attack), new Sequence(Patrol) })`.
