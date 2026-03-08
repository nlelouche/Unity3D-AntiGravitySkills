---
name: ai-code-reviewer
description: "Agentic code review checklist for Unity C# scripts. Identifies SOLID violations, GC allocation anti-patterns, naked Singletons, missing null guards, and architectural smells before human review."
version: 2.0.0
tags: ["tooling", "code-review", "quality", "architecture", "automation", "agentic", "SOLID"]
argument-hint: "action='review' target='Assets/Scripts/PlayerController.cs'"
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
  gc_alloc_per_frame: "N/A — static analysis tool"
  max_update_cost: "N/A — static analysis tool"
tdd_first: false
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - read_resource
  - mcp_unityMCP_find_in_file
  - mcp_unityMCP_validate_script
---

# AI Code Reviewer

## Overview
An agentic code review pass that reads a C# script and checks it against a structured checklist of Unity-specific and general engineering quality criteria. It produces a structured report of **CRITICAL**, **WARNING**, and **INFO** findings, mimicking a senior engineer's code review — before the code reaches human review.

## When to Use
- Use before committing a new feature to version control.
- Use after a code generation batch to verify generated code quality.
- Use during onboarding to enforce standards for new team members.
- ❌ Do NOT use as a replacement for human code review — use it to reduce the noise.

## Review Checklist

### 🔴 CRITICAL — Must Fix Before Merge

| ID | Check | Detection Pattern |
|----|-------|-------------------|
| C1 | `GetComponent` called in `Update()` | `Update.*GetComponent` regex |
| C2 | `new List/Array` allocation in `Update()` | `Update.*new (List\|Array\|\[\])` |
| C3 | `Find()` or `FindObjectOfType()` in `Update()` | `Update.*Find` |
| C4 | `public` field not `[SerializeField] private` | `^public (int\|float\|string\|bool)` |
| C5 | Naked Singleton (static instance, no DI) | `static.*Instance.*=.*this` |
| C6 | Empty Unity messages (`void Update() { }`) | `void (Update\|FixedUpdate)\(\) *\{ *\}` |
| C7 | Hardcoded magic string/number | `"[a-z]+[A-Z]"` in logic (non-const) |

### 🟡 WARNING — Should Fix

| ID | Check | Detection Pattern |
|----|-------|-------------------|
| W1 | LINQ in hot path | `\.Where\(\|\.Select\(\|\.FirstOrDefault` in Update |
| W2 | Missing null check after `GetComponent` | `GetComponent` not followed by `if.*null` |
| W3 | `string +=` in a loop | `string.*\+=.*` inside loop |
| W4 | Class has >300 lines (SRP violation) | Line count |
| W5 | Method has >30 lines (Single Responsibility) | Method line count |
| W6 | No namespace declaration | File start `^using` without `namespace` |
| W7 | TODO comment left in code | `//.*TODO` |

### 🔵 INFO — Consider Improving

| ID | Check |
|----|-------|
| I1 | Missing XML doc comment on public methods |
| I2 | Magic numbers not extracted to constants |
| I3 | MonoBehaviour without `[RequireComponent]` for dependencies |

## Review Procedure

1.  **Read the file**: Use `read_resource` or `view_file` to load the script.
2.  **Run each CRITICAL check** using `mcp_unityMCP_find_in_file` with the detection regex.
3.  **Run WARNING checks** similarly.
4.  **Compile Report**: Format findings as the Report Format below.
5.  **Provide Fix Suggestions**: For each CRITICAL, provide the corrected code snippet.

## Report Format

```
📋 CODE REVIEW — PlayerController.cs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 CRITICAL (2)
  [C1] Line 47: GetComponent<Rigidbody>() called inside Update()
       → Cache in Awake(): private Rigidbody _rb; → _rb = GetComponent<Rigidbody>();

  [C4] Line 12: public float Speed = 5f;
       → Change to: [SerializeField] private float _speed = 5f;

🟡 WARNING (1)
  [W6] No namespace found.
       → Add: namespace Game.Player { ... }

🔵 INFO (1)
  [I1] Public method Move() has no XML doc comment.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 6/10 — Needs fixes before merge
```

## Few-Shot Examples

### Example 1: Full Review Pass
**User**: "Review my PlayerController.cs before I commit it."

**Agent**:
1. Reads `PlayerController.cs`.
2. Runs `find_in_file` for `Update.*GetComponent` → finds line 47.
3. Runs `find_in_file` for `^public (int|float)` → finds 3 violations.
4. Outputs structured report with fix snippets for each CRITICAL.

### Example 2: Focused Check
**User**: "Check if there are any GC allocations in my Update methods."

**Agent**: Scans only for C1, C2, W1, W3 patterns and reports findings.

## Best Practices

- ✅ Run this **before** `@automated-unit-testing` — type errors from bad patterns can cascade.
- ✅ Always provide the corrected code snippet alongside each CRITICAL finding.
- ✅ Score the file: 0 CRITICALs = merge-ready; any = block.
- ❌ **NEVER** auto-apply fixes without confirming with the user.

## Related Skills

- `@unified-style-guide` — The standard this checker enforces
- `@automated-unit-testing` — Next step after a clean review
- `@unity-compile-fixer` — For compilation errors, not style smells
- `@coreclr-gc-watchdog` — For deep GC analysis beyond this checklist
