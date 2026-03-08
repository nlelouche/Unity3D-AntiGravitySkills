# 📐 AntiGravity Skill Master Template (2026 Standard)

> This is the **canonical reference template** for all skills in this repository.
> Use the `skill-creator` meta-skill to scaffold new skills from this template automatically.

---

## SKILL.md Template

```markdown
---
name: skill-name
description: "Expert, actionable one-liner describing what this skill generates or solves."
version: 2.0.0
tags: ["domain", "pattern", "keywords"]
argument-hint: "param='value' OR action='verb'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any | URP | HDRP | Built-in"
  dependencies: []           # e.g., ["com.unity.burst", "com.unity.inputsystem"]
context_discovery:
  check_unity_version: true
  check_render_pipeline: true
  scan_manifest_for: []      # packages to verify before activating
performance_budget:
  gc_alloc_per_frame: "0 bytes"
  max_update_cost: "O(1)"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# [Skill Title]

## Overview
[2–3 sentences: what it generates, what problem it solves, the key architectural decision.]

## When to Use
- Use when [symptom / trigger condition]
- Use when [symptom / trigger condition]
- Use instead of [anti-pattern this replaces]
- ❌ Do NOT use when [counter-indication]

## Architecture

[ASCII diagram or Mermaid showing the key components and their relationships]

## Components

| Component | Role |
|-----------|------|
| `IFoo` | Interface contract |
| `FooBase<T>` | Abstract base with boilerplate |
| `FooManager` | Orchestrates lifecycle |

## Context Discovery Checklist

Before generating code, confirm:
- [ ] Unity version: `>=6.0` → enables `Awaitable`, `ObjectPool<T>`, etc.
- [ ] Render Pipeline: [URP / HDRP / Any]
- [ ] Packages: `com.unity.package` present in `manifest.json`

## Procedure

1. **[Step 1]**: [What to do]
2. **[Step 2]**: [What to do]
3. **[Step 3]**: [What to do]

## Best Practices

- ✅ [Positive rule]
- ✅ [Positive rule]
- ❌ **NEVER** [Negative rule]
- ❌ **NEVER** [Negative rule]

## TDD Contract

```csharp
// Write these tests BEFORE implementing:
[Test]
public void FeatureName_WhenCondition_ThenExpectedBehavior()
{
    // Arrange
    // Act
    // Assert
}
```

## Few-Shot Examples

### Example 1: [Most common use case]
**User**: "[Typical user prompt]"

**Agent**:
```csharp
// Canonical implementation here
```

### Example 2: [Edge case or advanced use]
**User**: "[Second typical prompt]"

**Agent**:
```csharp
// Variant implementation
```

## Performance Notes

| Scenario | Without Skill | With Skill |
|----------|:---:|:---:|
| [Metric] | [Bad value] | [Good value] |

## Related Skills

- `@related-skill-1` — [Why it relates]
- `@related-skill-2` — [Why it relates]

## Template Files

- `templates/IFoo.cs.txt` — Core interface
- `templates/FooBase.cs.txt` — Abstract base
- `templates/FooManager.cs.txt` — Lifecycle manager
```

---

## YAML Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | kebab-case unique identifier |
| `description` | string | ✅ | One-liner, action-oriented |
| `version` | semver | ✅ | Start at `2.0.0` |
| `tags` | string[] | ✅ | For semantic search |
| `argument-hint` | string | ✅ | Example invocation params |
| `tier` | int (1-3) | ✅ | Always `2` for skill body |
| `requirements.unity_version` | string | ✅ | SemVer range (e.g. `>=6.0`) |
| `requirements.render_pipeline` | string | ✅ | `Any`, `URP`, `HDRP`, `Built-in` |
| `requirements.dependencies` | string[] | ✅ | Package IDs from manifest.json |
| `context_discovery.*` | bool | ✅ | Discovery checks to run |
| `performance_budget.*` | string | ✅ | GC alloc and CPU budget |
| `tdd_first` | bool | ✅ | Always `true` |

---

## Directory Structure Convention

```text
.agent/skills/{category}/{skill-name}/
├── SKILL.md                  # Tier 1 (YAML) + Tier 2 (body)
├── templates/                # Tier 3: code templates
│   ├── IFeature.cs.txt
│   ├── FeatureBase.cs.txt
│   └── FeatureManager.cs.txt
├── scripts/                  # (Optional) automation scripts
│   └── scaffold.py
└── references/               # (Optional) docs, diagrams, links
    └── notes.md
```

---

## Category Taxonomy

| Number | Folder | Domain |
|--------|--------|--------|
| `00-core-engineering` | Governance | C# standards, GC, coreclr |
| `00-meta-skills` | Meta | Skill creation, planning, scaffolding |
| `01-architecture` | Architecture | Patterns, FSM, DI, events |
| `02-gameplay` | Gameplay | Mechanics, AI, physics |
| `03-simulation-strategy` | Simulation | City builders, survival, strategy |
| `04-visuals-audio` | Visuals | Shaders, VFX, Cinemachine, Audio |
| `05-ui-ux` | Interface | UI Toolkit, MVVM, Input, A11y |
| `06-performance` | Performance | Jobs, Burst, pooling, profiling |
| `07-tools-pipeline` | Tooling | Editor tools, testing, import pipeline |
| `08-backend-monetization` | Backend | PlayFab, UGS, IAP, Ads, Netcode |
| `09-devops-automation` | DevOps | Build pipeline, CI/CD |
