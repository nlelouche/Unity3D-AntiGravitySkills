---
name: metadata-validator
description: "Audits all SKILL.md files in the repository for 2026 standard compliance. Reports missing YAML keys, outdated version fields, and broken Related Skills links."
version: 2.0.0
tags: ["tooling", "meta", "validation", "audit", "compliance", "automation"]
argument-hint: "action='audit' OR action='report' scope='all|category=01-architecture'"
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
  gc_alloc_per_frame: "N/A — Editor/CLI tool"
  max_update_cost: "N/A — one-shot audit"
tdd_first: false
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - read_resource
  - write_to_file
---

# Metadata Validator

## Overview
The **Metadata Validator** is an audit tool that scans every `SKILL.md` file in the repository and verifies they conform to the **2026 AntiGravity Standard** (as defined in `SKILL_MASTER_TEMPLATE.md`). It produces a compliance report listing every file that is missing required YAML fields, referencing outdated Unity versions, or containing broken `@skill-name` links in "Related Skills" sections.

## When to Use
- Use after adding new skills to verify they pass the standard.
- Use periodically as a health check on the skill library.
- Use before a major release / version bump.
- Use after an agent batch edit to confirm no files were corrupted.

## Compliance Checklist (per SKILL.md)

| Check | Key / Pattern | Expected |
|-------|--------------|---------|
| Has `name:` | YAML `name:` | Present, not empty |
| Has `version:` | YAML `version:` | `2.x.x` semver |
| Has `requirements:` block | YAML `requirements:` | Present |
| Has `unity_version:` | YAML `unity_version:` | `>=6.0` or specific |
| Has `context_discovery:` block | YAML `context_discovery:` | Present |
| Has `performance_budget:` block | YAML `performance_budget:` | Present |
| Has `tdd_first:` | YAML `tdd_first:` | `true` or `false` |
| Has `## Overview` | Markdown | H2 section present |
| Has `## When to Use` | Markdown | H2 section present |
| Has `## Best Practices` | Markdown | H2 section present |
| Has `## Related Skills` | Markdown | H2 section present |
| No proprietary references | grep "Project Noir" | 0 matches |

## Audit Procedure

### PowerShell (Windows — Recommended)

```powershell
# Run from the repo root (d:\AntiGravitySkills)
$results = @()

Get-ChildItem -Recurse -Filter "SKILL.md" ".agent/skills" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $missing = @()

    if ($content -notmatch "requirements:")        { $missing += "requirements" }
    if ($content -notmatch "context_discovery:")   { $missing += "context_discovery" }
    if ($content -notmatch "performance_budget:")  { $missing += "performance_budget" }
    if ($content -notmatch "tdd_first:")           { $missing += "tdd_first" }
    if ($content -notmatch "version: 2")           { $missing += "version>=2.0" }
    if ($content -notmatch "## Overview")          { $missing += "## Overview" }
    if ($content -notmatch "## When to Use")       { $missing += "## When to Use" }
    if ($content -notmatch "## Best Practices")    { $missing += "## Best Practices" }
    if ($content -notmatch "## Related Skills")    { $missing += "## Related Skills" }
    if ($content -match "Project Noir")            { $missing += "PROPRIETARY REF!" }

    $status = if ($missing.Count -eq 0) { "✅ PASS" } else { "❌ FAIL" }
    $results += [PSCustomObject]@{
        Status  = $status
        File    = $_.FullName.Replace("$PWD\", "")
        Missing = ($missing -join ", ")
    }
}

# Print report
$results | Format-Table -AutoSize
$passed  = ($results | Where-Object Status -eq "✅ PASS").Count
$failed  = ($results | Where-Object Status -eq "❌ FAIL").Count
Write-Host "`n📊 COMPLIANCE REPORT: $passed PASS | $failed FAIL" -ForegroundColor Cyan

# Export to file
$results | Export-Csv -Path "audit_report.csv" -NoTypeInformation
```

### Python Alternative

```python
import os, re

required_yaml   = ["requirements:", "context_discovery:", "performance_budget:", "tdd_first:"]
required_md     = ["## Overview", "## When to Use", "## Best Practices", "## Related Skills"]
proprietary     = ["Project Noir"]

results = []
for root, _, files in os.walk(".agent/skills"):
    for f in files:
        if f.lower() != "skill.md":
            continue
        path    = os.path.join(root, f)
        content = open(path, encoding="utf-8").read()
        missing = []
        for key in required_yaml + required_md:
            if key not in content:
                missing.append(key)
        if "version: 2" not in content:
            missing.append("version>=2.0")
        for term in proprietary:
            if term in content:
                missing.append(f"PROPRIETARY:{term}")
        results.append({"path": path, "missing": missing})

passed = sum(1 for r in results if not r["missing"])
print(f"\n📊 COMPLIANCE: {passed} PASS | {len(results)-passed} FAIL\n")
for r in results:
    status = "✅" if not r["missing"] else "❌"
    print(f"{status} {r['path']}")
    for m in r["missing"]:
        print(f"   └─ Missing: {m}")
```

## Interpreting the Report

| Status | Meaning | Action |
|--------|---------|--------|
| `✅ PASS` | Fully compliant | No action needed |
| `❌ FAIL — requirements` | Missing YAML block | Add `requirements:` block from template |
| `❌ FAIL — version>=2.0` | Still on v1.x | Bump `version: 2.0.0` |
| `❌ FAIL — PROPRIETARY` | Contains locked references | Remove/generalize the reference |

## Best Practices

- ✅ Run this after every **skill batch edit** to catch regressions.
- ✅ Add the PowerShell script to `Initialize.ps1` as an optional step.
- ✅ Export to `audit_report.csv` and commit it as a compliance artifact.
- ❌ **NEVER** skip this validation before a version tag / release.

## Related Skills

- `@skill-creator` — Creates new skills pre-compliant with this validator
- `@unified-style-guide` — The style standard this validator enforces
- `@context-discovery-agent` — Companion for runtime project validation
