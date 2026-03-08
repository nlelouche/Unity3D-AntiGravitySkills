---
name: build-pipeline-manager
description: "Command Line Interface (CLI) wrapper for automating Unity Builds (Android, iOS, Windows). Essential for CI/CD (Jenkins, GitHub Actions)."
version: 2.0.0
tags: ["devops", "ci-cd", "build-automation", "cli", "jenkins"]
argument-hint: "platform='Android' version='1.0.2' output='Builds/APK'"
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
  gc_alloc_per_frame: "N/A - async or editor-only"
  max_update_cost: "N/A"
tdd_first: false
---

# Build Pipeline Manager

## Overview
Allows Unity to be "Headless" and built via command line. This skill provides the C# static methods to be called by Unity's `-executeMethod` flag, enabling automated builds for CI/CD.

## When to Use
- Use for GitHub Actions / GitLab CI pipelines.
- Use for building Nightly versions automatically.
- Use to switch between "Dev" (Debug) and "Prod" (Release) builds securely.
- Use to increment version numbers automatically.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CI SERVER (Bash/PowerShell)  UNITY EDITOR (Headless)       │
│  ┌───────────────────────┐   ┌───────────────────────────┐  │
│  │ "Unity.exe -batchmode"│──▶│ BuildCommand.Execute()    │  │
│  │ "-executeMethod Build"│   │ 1. Set Defines (PROD)     │  │
│  └───────────────────────┘   │ 2. Set Keystore Pass      │  │
│                              │ 3. BuildAddressables()    │  │
│                              │ 4. BuildPlayer()          │  │
│                              └─────────────┬─────────────┘  │
│                                            │                │
│                                            ▼                │
│                               ┌───────────────────────────┐ │
│                               │ ARTIFACT (APK / EXE)      │ │
│                               └───────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Accept arguments from command line (e.g., `-buildVersion 1.0`).
- ✅ Always build Addressables *before* the Player build.
- ✅ Fail fast: throw exceptions if Scenes are missing.
- ✅ Secrets Management: Read keystore passwords from Environment Variables, never hardcode.
- ❌ **NEVER** put `Editor` scripts in runtime assemblies (use `Editor/` folder).

## Few-Shot Examples

### Example 1: Build Method
**User**: "Create a build script for Android."

**Agent**:
```csharp
public static void BuildAndroid() 
{
    BuildPlayerOptions opts = new BuildPlayerOptions();
    opts.target = BuildTarget.Android;
    opts.locationPathName = "Builds/Game.apk";
    BuildPipeline.BuildPlayer(opts);
}
```

### Example 2: CLI Usage
**User**: "How do I run this?"

**Agent**:
```bash
"C:\Program Files\Unity\Hub\Editor\2022.3.0f1\Editor\Unity.exe" -quit -batchmode -projectPath "." -executeMethod BuildScript.BuildAndroid
```

## Related Skills
- `@version-control-git` - Source of the build
- `@addressables-asset-management` - Content build content
