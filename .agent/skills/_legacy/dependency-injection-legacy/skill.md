---
name: unity-dependency-injection-vcontainer
description: "Senior Architect for Dependency Injection and Service Management. Activate this skill when the user requests "connecting systems," "managing services," "setting up Managers," or when refactoring static Singletons (.Instance)."
version: 1.0.0
tags: []
---

# Dependency Injection (VContainer Agentic Standard 2.0)


## When to Use
- Use when quest tracking
- Use when objective systems
- Use when mission progression
## 🎯 Context & Goal
[cite_start]The objective is to eliminate tight coupling and hidden dependencies that lead to rigid, untestable code and runtime `NullReferenceExceptions`[cite: 164, 173]. [cite_start]This skill mandates the use of **VContainer** to manage object lifecycles and service registration, ensuring a "Clean Architecture" where logic is decoupled from Unity's API[cite: 164, 165].

## 🧠 Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating any code, the agent MUST perform and document the following analysis to ensure architectural integrity[cite: 32]:
1. [cite_start]**Scope Identification**: Determine if the dependency belongs to the global `ProjectLifetimeScope` (Cross-scene) or a specific `SceneLifetimeScope`[cite: 166, 170].
2. [cite_start]**Lifetime Selection**: Define the correct lifetime for each service: `Singleton` (One instance), `Transient` (New every time), or `Scoped`[cite: 171].
3. [cite_start]**Abstraction Mapping**: Identify the required contracts (`interfaces`) for each service to ensure implementation-agnostic logic[cite: 169].
4. [cite_start]**Injection Strategy**: Decide between Constructor Injection (for pure C# classes) or Method/Setter Injection (for MonoBehaviours using `[Inject]`).

## 🛠️ Operational Procedure (Step-by-Step)
1.  [cite_start]**Artifact Generation (Dependency & Lifetime Map)**: Emit a structured plan listing all services to be registered, their intended lifetimes, and their consumers before writing implementation code[cite: 32].
2.  [cite_start]**Interface Definition**: Create clean interfaces (e.g., `IEconomyService`) isolated from concrete Unity implementations[cite: 169].
3.  [cite_start]**Installer Configuration**: Generate or modify the `Configure(IContainerBuilder builder)` method in the appropriate `LifetimeScope`[cite: 171].
4.  [cite_start]**Service Registration**: Map concrete implementations to their interfaces (e.g., `builder.Register<IEconomyService, EconomyManager>(Lifetime.Singleton)`)[cite: 171].
5.  **Injection Execution**: Apply `[Inject]` attributes or Constructor logic to consumers, ensuring zero reliance on static accessors.

## 🚫 Constraints & Prohibitions (Hard Rules)
- [cite_start]**FORBIDDEN**: Using `.Instance` (Singletons) to access systems that should be registered in the container[cite: 164].
- **FORBIDDEN**: Using `GameObject.Find`, `FindObjectOfType`, or `FindWithTag` for locating major systems.
- [cite_start]**MANDATORY**: Register services via their interfaces to maintain the Open/Closed Principle[cite: 171].
- [cite_start]**MANDATORY**: Every `LifetimeScope` must be validated for missing bindings during the "Agent Audit" phase to prevent runtime crashes.

## 📝 Artifact: Dependency & Injection Audit
[cite_start]The agent must verify the output against this checklist[cite: 30]:
- [ ] **Scope Alignment**: Are long-lived services correctly placed in the `ProjectLifetimeScope`?
- [ ] **Decoupling**: Are consumers requesting interfaces instead of concrete classes?
- [ ] **Binding Safety**: Has the `Configure` method been updated to include all new dependencies?

## 💡 Few-Shot Examples
- **User Input**: "Make the Quest System able to check the Player's inventory for required items."
- **Agent Output**: Generates a **Dependency Map** registering `IInventoryService` in the `SceneLifetimeScope`, followed by the injection of `IInventoryService` into the `QuestManager` constructor.