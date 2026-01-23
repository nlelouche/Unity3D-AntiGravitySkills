---
name: unity-scriptableobject-architecture
description: Senior Architect for Data-Driven Design. Activate this skill when the user requests "balancing stats," "global variables," "SO-based event channels," "item/building databases," or "persistent data containers."
---

# ScriptableObject Architecture (Agentic Production Standard 2.0)

## 🎯 Context & Goal
The objective is to decouple gameplay data and signals from MonoBehaviour logic, creating a flexible, data-driven architecture. [cite_start]This skill mandates the use of **ScriptableObjects (SO)** as the "Single Source of Truth" for design constants and event broadcasting, allowing the agent to perform autonomous balance passes and system refactoring without modifying core C# logic.

## 🧠 Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating assets, the agent MUST perform and document this "Agent-First" analysis[cite: 11]:
1. [cite_start]**Data vs. State Identification**: Distinguish between static design data (e.g., base health) and runtime state (e.g., current health)[cite: 129].
2. **Asset Hierarchy Planning**: Define a logical `CreateAssetMenu` structure to ensure human-readable organization.
3. **Dependency Mapping**: Identify which systems will consume the data and how they will be notified of changes (e.g., Game Events).
4. [cite_start]**Memory Management**: Assess if the SO contains heavy assets (Textures/Audio) that require `AssetReference` for Addressables integration[cite: 46].

## 🛠️ Operational Procedure (Step-by-Step)
1. [cite_start]**Artifact Generation (Data Schema Plan)**: Emit a structured plan detailing the SO class structure, fields, and intended menu paths before creating scripts[cite: 32].
2. **Container Definition**: Create classes inheriting from `ScriptableObject` with high-level validation attributes (e.g., `[Range]`, `[Min]`).
3. [cite_start]**Event Channel Implementation**: Implement `GameEventSO` patterns to allow "broadcast" communication between systems[cite: 8, 237].
4. [cite_start]**Runtime Set Management**: Use SOs to track collections of active scene objects (e.g., EnemyHordeSet) to avoid expensive `Find` calls[cite: 88].
5. [cite_start]**Reset Protocol**: Implement mandatory initialization logic to reset runtime variables during Editor playmode transitions[cite: 89].

## 🚫 Constraints & Prohibitions (Hard Rules)
- [cite_start]**FORBIDDEN**: Including heavy execution logic (Physics, Input, UI rendering) inside a ScriptableObject; they must remain data containers or signal hubs[cite: 88].
- **FORBIDDEN**: Using `GameObject.Find` to locate data that should be injected via a ScriptableObject reference.
- **MANDATORY**: Use `[SerializeField]` with private fields and public getter-only properties to ensure data integrity.
- **MANDATORY**: Scripts must include `[CreateAssetMenu]` with a clear, hierarchical path (e.g., "Project/Combat/HealthConfig").

## 📝 Artifact: Data & Event Mapping Audit
[cite_start]The agent must verify the output against this checklist[cite: 29]:
- [ ] **Data Integrity**: Are all sensitive fields private and properly serialized?
- [ ] **Clean Lifecycle**: Is the SO free from direct `MonoBehaviour` references that could cause memory leaks?
- [ ] **Usability**: Is the menu path organized for rapid designer iteration?

## 💡 Few-Shot Examples
- **User Input**: "Create a system to configure building costs and construction times for the city builder."
- **Agent Output**: Generates a **Data Schema Plan**, creates the `BuildingDataSO` script with serialized cost/time fields, and provides the menu path `Project/Economy/BuildingData`.