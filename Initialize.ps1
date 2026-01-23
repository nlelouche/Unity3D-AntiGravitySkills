<#
.SYNOPSIS
    Automates the setup of AntiGravity Skills when used as a submodule.
    
.DESCRIPTION
    This script detects if it is running within a submodule structure (e.g., .agent/antigravity)
    and automatically:
    1. Copies AGENT.md to the project root (if missing).
    2. Creates a Junction (Symlink) in .agent/skills pointing to this library's skills.
    
.USAGE
    Run this script once after cloning the repo or adding the submodule.
    .\Initialize.ps1
#>

$ScriptRoot = $PSScriptRoot
Write-Host "Initializing AntiGravity Skills from: $ScriptRoot" -ForegroundColor Cyan

# Attempt to locate the Project Root
# Assumption: This repo is usually at <ProjectRoot>/.agent/antigravity
# So ProjectRoot is ../..
$PossibleProjectRoot = Resolve-Path "$ScriptRoot/../.."

# Verify if it looks like a Unity project (optional check, but good for safety)
# We look for "Assets" folder or "ProjectSettings"
if ((Test-Path "$PossibleProjectRoot/Assets") -or (Test-Path "$PossibleProjectRoot/ProjectSettings")) {
    $ProjectRoot = $PossibleProjectRoot
    Write-Host "Project Root detected at: $ProjectRoot" -ForegroundColor Green
} else {
    # Fallback/Warning if structure is different
    Write-Host "Warning: Could not strictly verify Unity Project Root at ../.." -ForegroundColor Yellow
    Write-Host "Assuming $PossibleProjectRoot is the intended target."
    $ProjectRoot = $PossibleProjectRoot
}

# --- 1. Setup AGENT.md ---
$SourceAgentMd = Join-Path $ScriptRoot "AGENT.md"
$TargetAgentMd = Join-Path $ProjectRoot "AGENT.md"

if (Test-Path $SourceAgentMd) {
    if (-not (Test-Path $TargetAgentMd)) {
        Copy-Item -Path $SourceAgentMd -Destination $TargetAgentMd
        Write-Host "[+] Copied AGENT.md to Project Root." -ForegroundColor Green
    } else {
        Write-Host "[-] AGENT.md already exists in Project Root. Skipping." -ForegroundColor Gray
    }
} else {
    Write-Host "[!] Error: Source AGENT.md not found in $ScriptRoot" -ForegroundColor Red
}

# --- 2. Setup .agent/skills Symlink ---
$SourceSkillsDir = Join-Path $ScriptRoot ".agent/skills"
$TargetAgentDir = Join-Path $ProjectRoot ".agent"
$TargetSkillsDir = Join-Path $TargetAgentDir "skills"

# Ensure .agent folder exists in project root
if (-not (Test-Path $TargetAgentDir)) {
    New-Item -ItemType Directory -Path $TargetAgentDir -Force | Out-Null
    Write-Host "[+] Created '$TargetAgentDir' directory." -ForegroundColor Green
}

# Create Junction/Symlink
if (Test-Path $TargetSkillsDir) {
    Write-Host "[-] '$TargetSkillsDir' already exists. Skipping link creation." -ForegroundColor Gray
} else {
    if (Test-Path $SourceSkillsDir) {
        # Create Junction (Admin rights not usually required for Junctions on local drives)
        New-Item -ItemType Junction -Path $TargetSkillsDir -Target $SourceSkillsDir | Out-Null
        Write-Host "[+] Created Junction: $TargetSkillsDir -> $SourceSkillsDir" -ForegroundColor Green
    } else {
        Write-Host "[!] Error: Skills source directory not found at $SourceSkillsDir" -ForegroundColor Red
    }
}

# --- 3. Optional: Add to .gitignore ---
$GitIgnorePath = Join-Path $ProjectRoot ".gitignore"
if (Test-Path $GitIgnorePath) {
    $GitIgnoreContent = Get-Content $GitIgnorePath
    $NeedsUpdate = $false
    
    # Check for AGENT.md ignore
    # (Optional: Users might WANT to version AGENT.md if they customize it. 
    #  For now, let's NOT automatically ignore AGENT.md to allow customization tracking)
    
    # Check for .agent/skills ignore (Since it's a junction, we might want to ignore the folder entry itself?
    # Git usually ignores directories that are junctions/symlinks unless added)
    # But usually good practice to ignore generated artifacts.
    
    # Recommendation only
    Write-Host "`n[i] Recommendation: Ensure your .gitignore handles these files as preferred." -ForegroundColor Cyan
}

Write-Host "`nAntiGravity Setup Complete! 🚀" -ForegroundColor Green
