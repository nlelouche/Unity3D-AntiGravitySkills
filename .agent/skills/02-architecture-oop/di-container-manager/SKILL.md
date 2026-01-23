---
name: di-container-manager
description: strictly for OOP projects. Manages Dependency Injection (VContainer). Use to "create installers", "register services", or "refactor singletons".
argument-hint: "action='generate_installer' output='Assets/Scripts/MainScope.cs'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# DI Container Manager (OOP Architect)

## Goal
To enforce a robust OOP architecture using **Dependency Injection** (VContainer). This skill prevents the "Singleton Hell" typical of novice Unity projects and ensures high testability.

## Context
This is the **Core OOP Skill**. Unlike DOTS (which uses pure data), this skill manages **Objects** and **Services**.
It connects seamlessly with `service-layer-generator` and `ui-toolkit-architect`.

## Capabilities
1.  **Analysis**: Scans `Assets/Scripts` for classes named `*Service` or `*Manager`.
2.  **Generation**: Creates `LifetimeScope` (Installer) files automatically.
3.  **Refactoring**: Can advise on how to convert `ClassName.Instance` calls into `[Inject]` patterns.

## Procedure

### Scenario A: Setup Project DI
1.  **Check**: Look for existing `LifetimeScope`.
2.  **Action**: If none, run `python scripts/di_helper.py --action generate`.
3.  **Result**: Creates `GameLifetimeScope.cs` with all detected services auto-registered.

### Scenario B: Register a New Service
1.  **User**: "I added InventoryService. Wire it up."
2.  **Plan**: Identify `InventoryService` and its interface `IInventoryService`.
3.  **Edit**: Append `builder.Register<InventoryService>(Lifetime.Singleton).As<IInventoryService>();` to the active scope.

## Rules
- **No Singletons**: If you see `public static Type Instance`, mark it for DESTRUCTION.
- **Constructor Injection**: Prefer `[Inject]` on constructors for non-MonoBehaviours.
- **Method Injection**: Use `[Inject] public void Construct(...)` for MonoBehaviours.

## References
Read `references/vcontainer_guide.md` for proper syntax.
