---
name: service-layer-generator
description: "Generates Backend Service interfaces and implementations. Use to "create auth service", "mock network layer", or "add playfab service"."
version: 1.0.0
tags: []
argument-hint: service_name='AuthService' namespace='Game.Services'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Service Layer Generator

## Goal
To decouple game logic from external APIs (PlayFab, Firebase, Custom Backend). We generate an **Interface** (`IService`) and an **Implementation** (`Service`) that can be injected via VContainer.

## When to Use
- Use when defining contracts between systems
- Use when implementing dependency injection
- Use when creating testable code
- Use when PlayFab integration
- Use when backend services

## Architecture
- **Interface**: Defines *what* the service does.
- **Implementation**: Defines *how* (REST, SDK, Mock).
- **Rule**: Game Logic ONLY talks to the Interface.

## Procedure
1.  **Analyze**: Determine the scope (Auth, Inventory, Leaderboard).
2.  **Generate**: Create `I{Name}.cs` and `{Name}Impl.cs` in `Assets/Scripts/Services/`.
3.  **Suggest**: Remind the user to register this new service using `di-container-manager`.

## Few-Shot Example
User: "Create a Login Service."
Agent:
1.  Generates `ILoginService.cs` (Methods: `LoginAsync`, `Logout`).
2.  Generates `MockLoginService.cs` (Fake success after 1 second).
3.  User can then swap Mock for Real implementation later.
