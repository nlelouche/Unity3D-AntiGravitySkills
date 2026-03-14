---
name: version-control-git
description: "Best practices for Unity Git workflows, LFS configuration, and branching strategies."
version: 2.0.0
tags: ["git", "version-control", "lfs", "workflow", "collaborative"]
argument-hint: "action='gitignore' OR config='LFS' strategy='gitflow'"
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

# Version Control Git

## Overview
Setup and maintenance of robust Git workflows for Unity projects. Includes optimized `.gitignore` configuration, Git LFS (Large File Storage) for binary assets, and collaboration strategies.

## When to Use
- Use at project setup
- Use when binary assets (Texture, Audio) exceed 100MB
- Use when collaborating with teams
- Use when setting up CI/CD
- Use for branching and merging strategies

## Key Configurations

| File | Purpose |
|------|---------|
| **.gitignore** | Excludes temp/generated files (Library, Temp, Logs) |
| **.gitattributes** | Defines LFS tracking (DLL, PNG, WAV, FBX) |
| **.gitmodules** | Manages submodules (Plugins, AntiGravity) |

## Unity Git Best Practices
- ✅ **YAML Serialization**: Unity Editor -> Edit -> Project Settings -> Editor -> Asset Serialization -> Force Text.
- ✅ **Visible Meta Files**: Unity Editor -> Edit -> Project Settings -> Version Control -> Mode -> Visible Meta Files.
- ✅ **LFS**: Always track binary files with LFS to keep repo size distinct from history size.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GIT LFS WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LOCAL REPO               REMOTE REPO (GitHub/GitLab)       │
│  ┌──────────────┐        ┌──────────────┐                   │
│  │ Source (.cs) │───────▶│ Source (.cs) │ (History)         │
│  │ Meta Files   │        │ Meta Files   │                   │
│  │              │        └──────────────┘                   │
│  │ LFS Pointer  │───────────────┐                           │
│  └──────┬───────┘               │                           │
│         │                       ▼                           │
│         │                ┌──────────────┐                   │
│         └───────────────▶│ LFS STORAGE  │ (Binaries)        │
│    (Actual Binary)       │ .psd .fbx    │                   │
│                          └──────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Few-Shot Examples

### Example 1: Unity .gitignore
**User**: "Generate gitignore for Unity."

**Agent**:
```gitignore
# Unity generated
/[Ll]ibrary/
/[Tt]emp/
/[Oo]bj/
/[Bb]uild/
/[Bb]uilds/
/[Ll]ogs/
/[Uu]ser[Ss]ettings/

# Visual Studio / Rider
.vs/
.idea/
*.csproj
*.sln
*.user
*.suo

# OS generated
.DS_Store
Thumbs.db
```

### Example 2: .gitattributes (LFS)
**User**: "Setup LFS for textures and models."

**Agent**:
```gitattributes
# Image formats
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text
*.tga filter=lfs diff=lfs merge=lfs -text

# Audio formats
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text

# 3D formats
*.fbx filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text

# Unity binaries
*.unitypackage filter=lfs diff=lfs merge=lfs -text
*.dll filter=lfs diff=lfs merge=lfs -text
```

### Example 3: Branching Strategy
**User**: "Explain GitFlow for our team."

**Agent**:
```
1. main: Production-ready code.
2. develop: Integration branch for features.
3. feature/feature-name: Individual developer work.
4. release/v1.0: Preparation for release (bug fixes only).
5. hotfix/critical-bug: Urgent fixes for main.

Rules:
- Never push to main/develop directly.
- Use Pull Requests (PRs) for code review.
- Squash commits when merging feature branches to keep history clean.
```

## Related Skills
- `@tools-pipeline` - CI/CD setup
- `@unity-mcp-connector` - Editor integration

## Best Practices
- Follow the patterns and constraints documented in this skill.
- Always run @context-discovery-agent before applying this skill to verify environment compatibility.
- Apply TDD where applicable: write the interface contract first, then implement.
- Zero GC in hot paths: cache references, avoid LINQ and 
ew allocations in Update loops.