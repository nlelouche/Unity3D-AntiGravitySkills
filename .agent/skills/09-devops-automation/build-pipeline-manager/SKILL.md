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
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
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



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void BuildPipelineManager_Should{ExpectedBehavior}_When{Condition}()
{{
    // Arrange
    // TODO: Setup test fixtures
    
    // Act
    // TODO: Execute system under test
    
    // Assert
    Assert.Fail("Not implemented — write test first");
}}

// Test 2: should handle [edge case]
[Test]
public void BuildPipelineManager_ShouldHandle{EdgeCase}()
{{
    // Arrange
    // TODO: Setup edge case scenario
    
    // Act
    // TODO: Execute
    
    // Assert
    Assert.Fail("Not implemented");
}}

// Test 3: should throw when [invalid input]
[Test]
public void BuildPipelineManager_ShouldThrow_When{InvalidInput}()
{{
    // Arrange
    var invalidInput = default;
    
    // Act & Assert
    Assert.Throws<Exception>(() => {{ /* execute */ }});
}}
```

### Pasos para completar el TDD:

1. **Descomenta** los tests above
2. **Implementa** la funcionalidad mínima para que compile
3. **Ejecuta** los tests — deben fallar (RED)
4. **Implementa** la funcionalidad real
5. **Verifica** que los tests pasen (GREEN)
6. **Refactorea** manteniendo los tests verdes

---

**Nota**: Este skill fue marcado como `tdd_first: false` durante la auditoría v2.0.1. La sección TDD fue agregada automáticamente pero requiere customización manual para reflejar el comportamiento real del skill.


## Related Skills
- `@version-control-git` - Source of the build
- `@addressables-asset-management` - Content build content
