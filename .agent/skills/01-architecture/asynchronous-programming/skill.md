---
name: unity-asynchronous-programming
description: Lead Architect for Non-Blocking Operations and Concurrency. Activate this skill for handling "loading sequences", "network/API calls", "gameplay timers", "heavy CPU calculations", or "Main Thread optimization".
---

# Asynchronous Programming (Agentic Production Standard)

## ?? Context & Goal
The objective is to ensure 60+ FPS gameplay by offloading time-consuming tasks from the Unity Main Thread without compromising memory safety. [cite_start]This skill mandates the use of **UniTask** and **async/await** patterns to eliminate frame stutters, managing the complex lifecycle of game objects and avoiding "zombie" background tasks through strict cancellation protocols[cite: 8].

## ?? Thinking Process (Mandatory Internal Reasoning)
[cite_start]Before generating any code, the agent MUST perform and document the following analysis to calibrate user trust[cite: 27]:
1. **Task Classification**: Is the task I/O-bound (file/network) or CPU-bound (complex math)?
2. **Context Awareness**: Does the task require returning to the Main Thread to interact with Unity's API (e.g., `Transform`, `GameObject`)?
3. [cite_start]**Cancellation Strategy**: Identify the "Owner" of the task and determine which `CancellationToken` (e.g., `GetCancellationTokenOnDestroy`) will prevent memory leaks[cite: 88].
4. [cite_start]**GC Pressure Assessment**: Verify if the operation minimizes heap allocations by using value-type `UniTask` instead of the standard `Task`.

## ??? Operational Procedure (Step-by-Step)
1.  [cite_start]**Artifact Generation (Concurrency & Lifecycle Plan)**: Emit a structured plan detailing the task's entry point, wait points (`await`), and error-handling strategy before writing implementation code[cite: 32].
2.  **UniTask Implementation**: Prioritize `UniTask` over C# `Task` for zero-allocation performance in Unity loops.
3.  [cite_start]**Token Plumbing**: Pass a `CancellationToken` through every asynchronous method in the chain[cite: 89].
4.  **Thread Migration**: For heavy calculations (e.g., City Builder economy or Horde pathfinding), use `await UniTask.RunOnThreadPool()` to offload work.
5.  **Main Thread Re-entry**: Use `await UniTask.SwitchToMainThread()` before accessing any `UnityEngine` components.

## ?? Constraints & Prohibitions (Hard Rules)
- **FORBIDDEN**: Using `async void`. You must use `async UniTaskVoid` for fire-and-forget or `async UniTask` for trackable tasks.
- [cite_start]**FORBIDDEN**: Calling `.Result` or `.Wait()` on tasks, as this causes immediate deadlocks in the Unity Editor and Player[cite: 88].
- **MANDATORY**: Wrap asynchronous blocks in `try-catch` and specifically handle `OperationCanceledException` to ensure clean task termination.
- **MANDATORY**: Check `if (this == null)` or use the `CancellationToken` after every `await` point to ensure the object still exists before proceeding.

## ?? Artifact: Concurrency & Performance Audit
[cite_start]The agent must verify the output against this checklist[cite: 30]:
- [ ] **Memory Safety**: Is the task properly linked to the object's lifecycle via a `CancellationToken`?
- [ ] **Zero-Allocation**: Is `UniTask` used instead of `Task` to avoid GC spikes?
- [ ] **Fluidity**: Does the task avoid blocking the Main Thread for more than 1ms?

## ?? Few-Shot Examples
- **User Input**: "Create a system that saves the game state to a file without freezing the screen."
- **Agent Output**: Generates a **Concurrency Plan**, then implements a `public async UniTask SaveGameAsync(CancellationToken ct)` using `UniTask.RunOnThreadPool()` for serialization and `await File.WriteAllTextAsync(...)`.