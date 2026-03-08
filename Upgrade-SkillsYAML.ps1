# Upgrade-SkillsYAML.ps1
# Phase 1: Insert 2026-standard YAML blocks into all legacy SKILL.md files
param(
    [string]$SkillsRoot = ".agent/skills",
    [switch]$DryRun = $false
)

$rpCategories = @("04-visuals-audio", "06-performance")
$skills = Get-ChildItem -Recurse -Filter "SKILL.md" $SkillsRoot
$upgraded = 0
$skipped = 0
$errors = 0

foreach ($skill in $skills) {
    $content = Get-Content $skill.FullName -Raw -Encoding UTF8

    if ($content -match "requirements:") {
        $skipped++
        continue
    }

    $segments = $skill.FullName -split [regex]::Escape([System.IO.Path]::DirectorySeparatorChar)
    $category = ($segments | Where-Object { $_ -match "^\d{2}-" } | Select-Object -First 1)

    $checkRP = "false"
    if ($rpCategories -contains $category) { $checkRP = "true" }

    $gcBudget = "0 bytes target in hot paths"
    $timeBudget = "O(n) - profiler-guided"
    if ($category -eq "06-performance") {
        $gcBudget = "0 bytes (target)"
        $timeBudget = "Profiler-verified"
    }
    if ($category -match "08-backend|09-devops") {
        $gcBudget = "N/A - async or editor-only"
        $timeBudget = "N/A"
    }

    $lines = $content -split "`r?`n"
    $closingIdx = -1
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i].Trim() -eq "---") {
            $closingIdx = $i
            break
        }
    }

    if ($closingIdx -eq -1) {
        Write-Host "WARNING no closing --- : $($skill.FullName)" -ForegroundColor Yellow
        $errors++
        continue
    }

    $lines = $lines | ForEach-Object {
        if ($_ -match "^version:\s+1\.\d+\.\d+") { "version: 2.0.0" } else { $_ }
    }

    $yamlLines = @(
        "requirements:",
        "  unity_version: `">=6.0`"",
        "  render_pipeline: `"Any`"",
        "  dependencies: []",
        "context_discovery:",
        "  check_unity_version: true",
        "  check_render_pipeline: $checkRP",
        "  scan_manifest_for: []",
        "performance_budget:",
        "  gc_alloc_per_frame: `"$gcBudget`"",
        "  max_update_cost: `"$timeBudget`"",
        "tdd_first: false"
    )

    $before = $lines[0..($closingIdx - 1)] -join "`n"
    $middle = $yamlLines -join "`n"
    $after = $lines[$closingIdx..($lines.Count - 1)] -join "`n"
    $newContent = $before + "`n" + $middle + "`n" + $after

    if ($DryRun) {
        $relPath = $skill.FullName.Replace($PWD.Path + "\", "")
        Write-Host "DRY-RUN: $relPath [$category]"
    }
    else {
        [System.IO.File]::WriteAllText($skill.FullName, $newContent, [System.Text.Encoding]::UTF8)
        $relPath = $skill.FullName.Replace($PWD.Path + "\", "")
        Write-Host "OK $relPath" -ForegroundColor Green
    }
    $upgraded++
}

Write-Host ""
Write-Host "=== YAML UPGRADE COMPLETE ===" -ForegroundColor Cyan
Write-Host "Upgraded : $upgraded"
Write-Host "Skipped  : $skipped"
Write-Host "Errors   : $errors"
