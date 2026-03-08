# Audit-Skills.ps1 — Final compliance check
$r_all = @("name:", "version: 2", "requirements:", "context_discovery:", "performance_budget:", "tdd_first:",
    "## Overview", "## When to Use", "## Best Practices", "## Related Skills")

$skills = Get-ChildItem -Recurse -Filter "SKILL.md" ".agent/skills"
$p = 0; $f = 0

foreach ($s in $skills) {
    $c = Get-Content $s.FullName -Raw
    $miss = $r_all | Where-Object { $c -notmatch [regex]::Escape($_) }
    if ($miss.Count -eq 0) {
        $p++
    }
    else {
        $f++
        $rel = $s.FullName -replace [regex]::Escape($PWD.Path + "\"), ""
        Write-Host "FAIL: $rel"
        Write-Host "      $($miss -join ' | ')"
    }
}

Write-Host ""
Write-Host "=== CATEGORIES ===" 
Get-ChildItem ".agent/skills" -Directory | ForEach-Object {
    $n = (Get-ChildItem $_.FullName -Recurse -Filter "SKILL.md").Count
    Write-Host "  $($_.Name) : $n skills"
}

Write-Host ""
$v2 = (Get-ChildItem -Recurse -Filter "SKILL.md" ".agent/skills" | Select-String "^version: 2" -List).Count
$v1 = (Get-ChildItem -Recurse -Filter "SKILL.md" ".agent/skills" | Select-String "^version: 1" -List).Count
Write-Host "=== VERSION === v2:$v2  v1:$v1"

Write-Host ""
$prop = (Get-ChildItem -Recurse -Filter "SKILL.md" ".agent/skills" | Select-String "Project Noir" -List).Count
Write-Host "=== PROPRIETARY REFS === $prop found (should be 0)"

Write-Host ""
Write-Host "=== FINAL SCORE: $p PASS  $f FAIL  $($skills.Count) total ==="
