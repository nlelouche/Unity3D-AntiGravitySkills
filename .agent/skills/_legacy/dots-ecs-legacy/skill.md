---
name: unity-dots-ecs-expert
description: "Principal Architect for Data-Oriented Design (DOD). [cite_start]Activate this skill when the user requests "processing thousands of entities," "massive performance optimization," "ECS implementation," or "Job System and Burst Compiler integration." [cite: 135, 136]"
version: 1.0.0
tags: []
---

# DOTS & ECS (Data-Oriented Production Standard 2.0)


## When to Use
- Use when implementing ECS systems
- Use when high-performance data-oriented code
- Use when DOTS/Burst optimization
- Use when quest tracking
- Use when objective systems
## 🎯 Context & Goal
[cite_start]The objective is to achieve massive CPU performance by eliminating MonoBehaviour overhead and cache misses through Data-Oriented Design[cite: 8, 130]. [cite_start]This skill mandates the implementation of **Entity Component System (ECS)**, the **Job System**, and the **Burst Compiler** to handle high-density simulations (e.g., massive enemy hordes) at 60+ FPS[cite: 132, 133].

## 🧠 Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating code, the agent MUST perform and document this internal analysis to ensure structural integrity[cite: 32, 84]:
1. [cite_start]**Data Layout Identification**: Define component data as unmanaged `structs` to ensure linear memory allocation[cite: 131, 140].
2. [cite_start]**System Type Selection**: Prioritize `ISystem` (unmanaged structs) over `SystemBase` (managed classes) for full Burst compatibility[cite: 139].
3. [cite_start]**Access Pattern Analysis**: Determine the safest and fastest query methods (`RefRW` for Read/Write vs. `RefRO` for Read-Only) to maximize parallelization safety[cite: 143].
4. [cite_start]**Baking Strategy**: Plan the `Baker<T>` implementation to bridge the gap between Authoring GameObjects and Runtime Entities[cite: 141, 143].

## 🛠️ Operational Procedure (Step-by-Step)
1.  [cite_start]**Artifact Generation (Performance & Data Layout Plan)**: Emit a plan detailing the component structures, the system's execution order, and the parallelization strategy before writing code[cite: 27, 32].
2.  [cite_start]**Component Definition**: Create `IComponentData` structs using only unmanaged types[cite: 137, 140].
3.  [cite_start]**ISystem Implementation**: Implement the system as a `partial struct` to allow source generators to work[cite: 140, 150].
4.  [cite_start]**Burst Optimization**: Apply the `[BurstCompile]` attribute to `OnCreate`, `OnUpdate`, and `OnDestroy` methods[cite: 141, 148].
5.  [cite_start]**Query & Job Execution**: Use `SystemAPI.Query<RefRW<T>, RefRO<U>>()` or `IJobEntity` for high-performance loops[cite: 143, 155].
6.  [cite_start]**Structural Changes**: Use `EntityCommandBuffer` (ECB) for creating or destroying entities within Jobs to prevent race conditions[cite: 144].

## 🚫 Constraints & Prohibitions (Hard Rules)
- [cite_start]**FORBIDDEN**: Using managed types (classes, strings, or standard C# arrays) within `IComponentData`[cite: 141].
- [cite_start]**FORBIDDEN**: Accessing `UnityEngine.Transform` inside an ECS System; use `Unity.Transforms.LocalTransform` instead[cite: 142, 149].
- [cite_start]**MANDATORY**: Use `state.RequireForUpdate<T>()` in `OnCreate` to prevent the system from running when no relevant entities exist[cite: 153, 154].
- [cite_start]**MANDATORY**: All systems must be `partial structs` inheriting from `ISystem`[cite: 140].

## 📝 Artifact: Performance & Burst Audit
[cite_start]The agent must verify the output against this checklist[cite: 30, 87]:
- [ ] [cite_start]**Burst Compatibility**: Is the system an unmanaged `struct` with `[BurstCompile]` on entry points? [cite: 141, 148]
- [ ] [cite_start]**Thread Safety**: Are all structural changes handled via `EntityCommandBuffer`? [cite: 144]
- [ ] [cite_start]**Memory Locality**: Are components grouped correctly to favor spatial locality in Chunks? [cite: 131]

## 💡 Few-Shot Examples
- [cite_start]**User Input**: "I need to move 10,000 projectiles in a straight line and check for collisions." [cite: 143]
- [cite_start]**Agent Output**: Generates a **Performance & Data Layout Plan**, followed by a `ProjectileComponent` struct, a `Baker`, and a Burst-compiled `ISystem` using `IJobEntity`. [cite: 141, 145]