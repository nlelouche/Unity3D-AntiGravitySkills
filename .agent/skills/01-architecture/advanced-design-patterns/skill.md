---
name: unity-advanced-design-patterns
description: Principal Architect for SOLID & GoF Patterns in Unity 3D. Activate this skill when the user requests complex systems, scalable mechanics, decoupled architectures, or when refactoring "God Classes" and circular dependencies.
---

# Advanced Design Patterns (Agentic Production Standard)

## 🎯 Context & Goal
[cite_start]The objective is to transform high-level gameplay requirements into modular, testable, and maintainable systems[cite: 8, 130]. [cite_start]This skill forces the agent to move away from "Spaghetti Code" by enforcing strict structural patterns (Strategy, Factory, Observer, Command) adapted for Unity's unique lifecycle and the 2026 production ecosystem[cite: 7, 164].

## 🧠 Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating any code, the agent MUST perform and document the following analysis[cite: 32]:
1. [cite_start]**Identify the Axis of Change**: Determine what part of the system is expected to vary (Behavior, Creation, or Notification)[cite: 130].
2. [cite_start]**Pattern Selection**: Justify the choice of pattern (e.g., Strategy for interchangeable logic, Factory for complex instantiation, Observer for decoupled UI/Events)[cite: 135].
3. [cite_start]**Unity Compatibility**: Assess if the pattern should be implemented via MonoBehaviours, ScriptableObjects, or pure C# classes (PoCO)[cite: 7, 88].
4. [cite_start]**SOLID Validation**: Ensure the proposed solution adheres to the Single Responsibility and Open/Closed principles[cite: 130, 164].

## 🛠️ Operational Procedure (Step-by-Step)
1.  [cite_start]**Artifact Generation (Implementation Plan)**: Emit a structured plan (Markdown or Mermaid) detailing the proposed class hierarchy and contracts before writing implementation code[cite: 32, 37].
2.  [cite_start]**Contract Definition**: Define interfaces (`IInterface`) or abstract classes (`BaseClass`) to establish strict API boundaries[cite: 140, 169].
3.  [cite_start]**Concrete Implementation**: Develop the specific logic classes, ensuring they are decoupled from the caller[cite: 157].
4.  [cite_start]**Dependency Resolution**: Use VContainer (DI) or ScriptableObject-based injection to resolve references, avoiding static Singletons[cite: 165, 171].
5.  [cite_start]**Audit Phase**: Self-correct the generated code against the "Constraints" section of this skill[cite: 206].

## 🚫 Constraints & Prohibitions (Hard Rules)
- [cite_start]**FORBIDDEN**: Using `GameObject.Find`, `SendMessage`, or `BroadcastMessage` for system communication[cite: 19, 88].
- [cite_start]**FORBIDDEN**: Large "switch" or "if-else" blocks for behavior selection; use Polymorphism/Strategy instead[cite: 138, 143].
- [cite_start]**MANDATORY**: Use `[SerializeField]` with private fields (`_camelCaseWithUnderscore`) for inspector references[cite: 88].
- [cite_start]**MANDATORY**: Interfaces must start with `I` (e.g., `IDamageable`)[cite: 139].
- [cite_start]**MANDATORY**: Every Factory implementation must support **Object Pooling** by default for high-frequency objects[cite: 121, 128].

## 📝 Artifact: Architecture & Performance Audit
The agent must verify the output against this checklist:
- [ ] [cite_start]**SRP Compliance**: Does each class have a single reason to change? [cite: 130]
- [ ] [cite_start]**Memory Safety**: Are events unsubscribed in `OnDisable`/`OnDestroy` to prevent memory leaks? [cite: 38]
- [ ] [cite_start]**Performance**: Is the pattern avoiding unnecessary heap allocations in `Update()` loops? [cite: 131, 141]

## 💡 Few-Shot Examples
- **User Input**: "I need a system for different enemy AI behaviors like patrolling, chasing, and retreating."
- **Agent Output**: Generates an **Implementation Plan** for the **Strategy Pattern**, followed by an `IEntityBehavior` interface and concrete classes (`PatrolBehavior`, `ChaseBehavior`), injected into an `EnemyController`.