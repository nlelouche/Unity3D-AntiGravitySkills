---
name: dots-system-architect
description: Generates high-performance, Burst-compatible ECS Systems using V2 Entities features (ISystem, IJobEntity). Accesses a library of optimized templates and best-practice references.
argument-hint: "action='create_system' name='MovementSystem' namespace='Game.Gameplay'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
  - view_file
---

# DOTS System Architect (Pro Edition)

## Goal
To act as a Senior ECS Engineer, providing not just code, but *architecturally sound* implementations using Unity's latest Data-Oriented Technology Stack.

## Capabilities
1.  **Code Generation**: Uses `templates/` to scaffold `ISystem` structs that are guaranteed to compile with Burst.
2.  **Validation**: Uses `scripts/burst_validator.py` to ensure user or agent code doesn't violate safety rules (e.g., managed types in jobs).
3.  **Education**: Can quote from `references/dots_best_practices.md` to explain *why* a certain approach (like `RefRO` vs `RefRW`) was chosen.

## Procedure

### Scenario A: Create a New System
1.  **Load Template**: Read `templates/SystemBurst_Template.cs.txt`.
2.  **Customize**: Replace placeholders (`{SYSTEM_NAME}`, `{NAMESPACE}`) with user arguments.
3.  **Propose Logic**: Insert the user's requested logic (e.g., "move character") into the `OnUpdate` loop, ensuring usage of `float3` and `SystemAPI.Time`.
4.  **Write File**: Save to `Assets/Scripts/Systems/{name}.cs`.

### Scenario B: Optimize Existing Code
1.  **Analyze**: Read the target file.
2.  **Validate**: Run `python scripts/burst_validator.py --file {path}`.
3.  **Refactor**:
    - If `class SystemBase` found -> Suggest migrating to `struct ISystem`.
    - If `foreach` found on main thread -> Suggest `IJobEntity` if loop body is heavy.
    - If `Vector3` found -> Replace with `float3` and `Unity.Mathematics`.

## Rules (The "Burst Commandments")
- **Thou shall not use Managed Types** (Classes) in Jobs.
- **Thou shall use RefRO** when Write access is not needed.
- **Thou shall use generic Math** (`math.abs` over `Mathf.Abs`).

## Few-Shot Example

**User**: "Create a system called 'CoinRotationSystem' that rotates coins."

**Agent**:
1.  Reads template.
2.  Fills `{SYSTEM_NAME}`="CoinRotationSystem".
3.  Fills `OnUpdate`:
    ```csharp
    var dt = SystemAPI.Time.DeltaTime;
    foreach (var transform in SystemAPI.Query<RefRW<LocalTransform>>().WithAll<CoinTag>()) {
        transform.ValueRW.RotateY(math.radians(90 * dt));
    }
    ```
4.  Writes file.
5.  Refers to `dots_best_practices.md` to mention why we used `RefRW`.
