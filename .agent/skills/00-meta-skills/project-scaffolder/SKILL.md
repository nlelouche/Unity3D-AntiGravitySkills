---
name: project-scaffolder
description: "Generates the initial folder structure, installs essential packages (Manifest), and configures project settings for a fresh Unity project."
version: 1.0.0
tags: ["meta", "setup", "initialization", "scaffold", "automation"]
argument-hint: "preset='3D_Action' OR preset='2D_Mobile'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Project Scaffolder

## Overview
Deploys a standard directory structure (`_Scripts`, `_Prefabs`, `Arts`) and modifies the `manifest.json` to install core packages like Input System, TextMeshPro, and Cinemachine immediately.

## When to Use
- Use immediately after creating a new Unity Project.
- Use to standardize folder hierarchy across team members.
- Use to install a "Stack" of packages in one go.

## Architecture

The scaffolder runs a script that:
1.  **Creates Folders**: `Assets/_Game`, `Assets/_Game/Scripts`, etc.
2.  **Edits Manifest**: Reads `Packages/manifest.json`, inserts dependencies, saves.
3.  **Creates README**: Adds a project overview.

## Best Practices
- ✅ Underscore core folders (`_Game`) to keep them at the top.
- ✅ Use `AssetDatabase.CreateFolder` to ensure .meta files are generated.
- ✅ Separate ThirdParty assets from own assets.
- ❌ **NEVER** overwrite existing folders without checking.

## Few-Shot Examples

### Example 1: Folder Structure
**User**: "Setup folders."

**Agent**:
```csharp
Directory.CreateDirectory(Application.dataPath + "/_Game");
Directory.CreateDirectory(Application.dataPath + "/_Game/Scripts");
AssetDatabase.Refresh();
```

## Related Skills
- `@skill-creator` - For creating skills
- `@version-control-git` - For initializing repo
