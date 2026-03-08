---
name: tech-tree-research
description: "Directed Acyclic Graph (DAG) based Tech Tree. Manages unlock states, prerequisites, and research costs."
version: 2.0.0
tags: ["tech-tree", "research", "upgrades", "progression", "graph"]
argument-hint: "action='Unlock' technology='Steel_Working'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: false
---

# Tech Tree & Research

## Overview
Manages a dependency graph of technologies/upgrades. Uses `ScriptableObjects` to define Nodes (Techs) and their Parents (Prerequisites).

## When to Use
- Use for Civ-like tech trees
- Use for RPG Skill Trees
- Use for unlocking buildings/units in RTS
- Use for persistent meta-progression
- Use for dependency validation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH GRAPH                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TECH NODE (SO)           RESEARCH MANAGER                  │
│  ┌────────────────┐      ┌───────────────────────────┐      │
│  │ Name: "Iron"   │      │ Unlocked: {Pottery, Iron} │      │
│  │ Cost: 50 Sci   │      │                           │      │
│  │ Parents: [Pot] │──────▶ IsUnlocked(Nodes)         │      │
│  └────────────────┘      │ CanResearch(Node)         │      │
│                          └─────────────┬─────────────┘      │
│                                        │                    │
│                                        ▼                    │
│                           ┌───────────────────────────┐     │
│                           │ EVENT: OnTechUnlocked     │     │
│                           └───────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Recursively check parents for `IsResearchable()`.
- ✅ Store `Visual` data (Icon, Description) in the Node SO.
- ✅ Store `State` (Unlocked/Available) in the Manager (Runtime).
- ✅ Use IDs or Object References for saving/loading.
- ❌ **NEVER** create cyclic dependencies (A requires B, B requires A). Editor Tools should validate this.
- ❌ **NEVER** hardcode tech trees in C# classes.

## Few-Shot Examples

### Example 1: Tech Node Data
**User**: "Create a tech node."

**Agent**:
```csharp
[CreateAssetMenu]
public class TechNode : ScriptableObject
{
    public string ID;
    public List<TechNode> Prerequisites;
    public int ResearchCost;
}
```

### Example 2: Validation Logic
**User**: "Check if I can research Steel."

**Agent**:
```csharp
public bool CanResearch(TechNode node)
{
    if (IsUnlocked(node)) return false;
    
    // All parents must be unlocked
    foreach (var parent in node.Prerequisites)
    {
        if (!IsUnlocked(parent)) return false;
    }
    
    return true;
}
```

## Related Skills
- `@resource-management-system` - Paying research costs
- `@save-load-serialization` - Saving unlocked tech
