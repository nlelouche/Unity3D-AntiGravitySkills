---
name: context-discovery-agent
description: "Auto-detects the Unity project environment (version, render pipeline, installed packages) and returns a structured context JSON consumed by all other skills before code generation."
version: 2.0.0
tags: ["tooling", "meta", "context", "discovery", "automation", "validation"]
argument-hint: "action='discover' OR action='report' output='context.json'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: false
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "N/A — Editor Tool"
  max_update_cost: "N/A — Editor Tool"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - read_resource
  - write_to_file
---

# Context Discovery Agent

## Overview
The **Context Discovery Agent** is the mandatory pre-flight skill. It reads the three key sources of truth in any Unity project — `ProjectVersion.txt`, the Render Pipeline asset, and `manifest.json` — and produces a structured `ContextReport` that all other skills consume before generating code. It eliminates the #1 cause of bad AI code: wrong assumptions about the environment.

## When to Use
- Use **automatically** at the start of every session or before any code generation.
- Use when a user reports "the code you gave me doesn't compile" (wrong package, wrong API).
- Use when switching between projects with different configurations.
- Use explicitly via `@context-discovery-agent action='discover'`.

## Architecture

```
┌────────────────────────────────────────────────────┐
│              CONTEXT DISCOVERY PIPELINE            │
├────────────────────────────────────────────────────┤
│                                                    │
│  SOURCE FILES           PARSED OUTPUT              │
│  ┌────────────────┐     ┌─────────────────────┐   │
│  │ProjectVersion  │────▶│ unity_version: 6.0  │   │
│  │  .txt          │     │ unity_major: 6       │   │
│  └────────────────┘     └─────────────────────┘   │
│                                                    │
│  ┌────────────────┐     ┌─────────────────────┐   │
│  │ Assets/Settings│────▶│ render_pipeline: URP│   │
│  │  *.asset files │     │ srp_version: 17.x   │   │
│  └────────────────┘     └─────────────────────┘   │
│                                                    │
│  ┌────────────────┐     ┌─────────────────────┐   │
│  │ Packages/      │────▶│ packages:           │   │
│  │  manifest.json │     │   burst: true       │   │
│  └────────────────┘     │   inputsystem: true │   │
│                          │   addressables: true│   │
│                          └─────────────────────┘   │
│                                                    │
│  FINAL OUTPUT → ContextReport (JSON)               │
└────────────────────────────────────────────────────┘
```

## Output Format (ContextReport)

```json
{
  "unity_version": "6000.0.30f1",
  "unity_major": 6,
  "render_pipeline": "URP",
  "srp_asset_path": "Assets/Settings/UniversalRenderPipelineAsset.asset",
  "packages": {
    "com.unity.burst": "1.8.19",
    "com.unity.collections": "2.5.1",
    "com.unity.inputsystem": "1.11.2",
    "com.unity.addressables": "2.3.1",
    "com.unity.netcode.gameobjects": null,
    "com.unity.entities": null,
    "com.unity.render-pipelines.universal": "17.0.3"
  },
  "features": {
    "awaitable_api": true,
    "burst_available": true,
    "jobs_available": true,
    "ecs_available": false,
    "new_input_system": true,
    "addressables_configured": true
  },
  "warnings": []
}
```

## Procedure

1.  **Read Unity Version**:
    ```
    File: ProjectSettings/ProjectVersion.txt
    Parse line: m_EditorVersion: 6000.0.30f1
    → unity_version = "6000.0.30f1", unity_major = 6
    ```

2.  **Detect Render Pipeline**:
    ```
    Scan: Assets/Settings/ for files matching *RenderPipelineAsset*.asset
    If found "UniversalRenderPipelineAsset" → URP
    If found "HDRenderPipelineAsset"        → HDRP
    If none found                           → Built-in
    ```

3.  **Parse Packages**:
    ```
    File: Packages/manifest.json
    Extract "dependencies" object
    Key packages to check:
      com.unity.burst
      com.unity.collections
      com.unity.jobs
      com.unity.inputsystem
      com.unity.addressables
      com.unity.netcode.gameobjects
      com.unity.entities
      com.unity.render-pipelines.universal
      com.unity.render-pipelines.high-definition
      com.unity.cinemachine
      com.unity.textmeshpro
    ```

4.  **Derive Feature Flags**:
    ```
    awaitable_api         = unity_major >= 6
    burst_available       = "com.unity.burst" in packages
    jobs_available        = "com.unity.collections" in packages
    ecs_available         = "com.unity.entities" in packages
    new_input_system      = "com.unity.inputsystem" in packages
    addressables_configured = "com.unity.addressables" in packages
    ```

5.  **Report to User**:
    ```
    ✅ Context validated:
       Unity 6.0 | URP 17.x
       Burst: ✅ | Jobs: ✅ | ECS: ❌ | Input System: ✅ | Addressables: ✅
    ```

## Best Practices

- ✅ Always run this **first** in a new session.
- ✅ Cache the ContextReport; re-run only if packages change.
- ✅ Use feature flags to gate skill suggestions (e.g., skip `@job-system-burst` if `burst_available: false`).
- ❌ **NEVER** assume the render pipeline — always detect it.
- ❌ **NEVER** assume Burst or Jobs are available without checking.
- ❌ **NEVER** use Unity 6 APIs (`Awaitable`) on projects with `unity_major < 6`.

## Few-Shot Examples

### Example 1: Discovering a URP Project
**User**: "Set up a shader for my character."

**Agent**: Runs Context Discovery → finds URP 17.x → automatically uses `Shader Graph (URP)` template instead of `Built-in` shader. Reports: `"✅ URP detected — using URP Shader Graph workflow."`

### Example 2: Missing Burst
**User**: "Implement the Job System skill for my pathfinding."

**Agent**: Runs Context Discovery → `burst_available: false` → "⚠️ The `job-system-burst` skill requires `com.unity.burst`. Please install it via Package Manager (Window → Package Manager → Add by name: `com.unity.burst`). I'll wait."

### Example 3: Built-in Render Pipeline Warning
**User**: "Add post-processing effects."

**Agent**: Detects Built-in RP → "ℹ️ Your project uses Built-in Render Pipeline. The modern `Volume` framework is only available in URP/HDRP. I'll use the legacy Post Processing Stack v2 approach. Shall I also provide a URP migration guide?"

## Related Skills

- `@unity-compile-fixer` — Uses context to validate package-related CS0234 errors
- `@job-system-burst` — Requires `burst_available: true`
- `@ui-toolkit-modern` — Requires `unity_major >= 6`
- `@addressables-asset-management` — Requires `addressables_configured: true`
