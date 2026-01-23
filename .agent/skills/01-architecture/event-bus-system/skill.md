---
name: unity-interface-driven-development
description: Senior Architect for Contract-Based Modularity (IDD). [cite_start]Activate this skill when the user requests "interchangeable systems," "shared behaviors," "decoupling Unity logic," or "Interface Segregation Principle implementation." [cite: 43, 76]
---

# Interface-Driven Development (Agentic Production Standard 2.0)

## 🎯 Context & Goal
[cite_start]The objective is to eliminate the rigidity of deep inheritance and hard-coupling to concrete classes. [cite_start]This skill mandates programming towards **Interfaces** (contracts), allowing the agent to autonomously expand game mechanics (e.g., new units, weapons, or buildings) by simply fulfilling pre-defined requirements[cite: 132, 161].

## 🧠 Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating code, the agent MUST perform and document this analysis to ensure architectural modularity[cite: 32]:
1. [cite_start]**Behavior Extraction**: Identify pure behaviors (e.g., `IDamageable`, `IInteractable`) before defining the object's identity[cite: 6].
2. [cite_start]**Contract Scoping**: Determine the minimum methods required for the interface (Interface Segregation)[cite: 7].
3. **Dependency Analysis**: Identify which high-level systems will consume this interface and how they will resolve the reference (DI vs. Inspector).
4. [cite_start]**Mockability**: Assess if the interface is simple enough to be mocked for automated unit testing[cite: 8, 205].

## 🛠️ Operational Procedure (Step-by-Step)
1. [cite_start]**Artifact Generation (Architecture Blueprint)**: Emit a structured plan detailing the proposed interfaces, their methods, and the consuming systems before implementation[cite: 32].
2. [cite_start]**Interface Definition**: Create small, specific interfaces following the SOLID principles[cite: 7].
3. [cite_start]**Decoupled Reference Implementation**: Use interfaces as reference types in consumer scripts, avoiding concrete class dependencies[cite: 8].
4. [cite_start]**Abstraction Guard**: Use `TryGetComponent<IInterface>(out var instance)` or DI containers to interact with objects safely[cite: 171, 173].
5. [cite_start]**Self-Correction Audit**: Verify the code against the "Constraints" section of this skill[cite: 206].

## 🚫 Constraints & Prohibitions (Hard Rules)
- [cite_start]**FORBIDDEN**: Using the "Base" suffix in classes (e.g., `EnemyBase`) if the functionality can be achieved via an Interface[cite: 88].
- [cite_start]**FORBIDDEN**: Casting an interface back to its concrete class; abstractions must be self-sufficient[cite: 88].
- [cite_start]**MANDATORY**: Naming Convention: All interfaces must start with the `I` prefix (e.g., `IInteractable`)[cite: 88].
- [cite_start]**MANDATORY**: Interfaces must reside in dedicated files to prevent circular dependencies during static agent analysis[cite: 52, 66].

## 📝 Artifact: Interface & Decoupling Audit
[cite_start]The agent must verify the output against this checklist[cite: 38]:
- [ ] **Segregation**: Does the interface define a single, clear behavior?
- [ ] **Neutrality**: Is the interface free from `MonoBehaviour` specific dependencies where possible?
- [ ] [cite_start]**Testability**: Is the contract robust enough for automated unit test generation? [cite: 199]

## [cite_start]💡 Few-Shot Examples [cite: 90]
- **User Input**: "I need a system where the player can damage both enemies and breakable walls using the same attack."
- **Agent Output**: Generates an **Architecture Blueprint** proposing the `IDamageable { void TakeDamage(float amount); }` interface, followed by implementations in `Enemy` and `DestructibleWall` classes.