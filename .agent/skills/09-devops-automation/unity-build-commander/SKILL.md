---
name: unity-build-commander
description: "Executes a headless Unity build for the target platform (Windows/Android/iOS), parses the Editor.log for compilation errors, and reports the build status. Use this when the user asks to "build the game" or "check for compile errors"."
version: 2.0.0
tags: []
argument-hint: target='StandaloneWindows64' build_path='Builds/Win64'
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
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

# Unity Build Commander

## Overview

## Goal
To autonomously execute a Unity build process via the CLI, capture the output logs, parse them for errors, and provide a definitive success/failure report. This allows the agent to verify its own code changes.

## When to Use
- Use when automated builds
- Use when CI/CD
- Use when build pipeline
- Use when custom inspectors
- Use when editor windows

## Constraints
- **Safety**: Do not overwrite critical project settings files.
- **Headless**: Always run with `-batchmode` and `-quit` to avoid opening the Unity Editor GUI.
- **Logging**: Must capture logs to a temporary file or stdout to parse errors.
- **Feedback**: If the build fails, you MUST report the specific compiler errors (Filename, Line Number, Error Message).

## Procedure

1.  **Identify Target**: Determine the build target (StandaloneWindows64, Android, iOS). Default to Windows if not specified.
2.  **Execute Build Wrapper**: Call the python script `scripts/build_wrapper.py`. This script handles the complex Unity CLI arguments and log parsing.
    - Command: `python .agent/skills/04-devops-automation/unity-build-commander/scripts/build_wrapper.py --target {target} --output {build_path}`
3.  **Analyze Result**: The script will output a JSON object to stdout.
    - If `status` is "success": Report the location of the build.
    - If `status` is "failure": List the top 3 errors and ask the user if they want you to fix them.

## Few-Shot Example

**User**: "Check if the code compiles."

**Agent**:
1.  Infers target: `StandaloneWindows64`.
2.  Runs: `python .../build_wrapper.py --target StandaloneWindows64 --check-only`
3.  Output: `{"status": "failure", "errors": [{"file": "PlayerController.cs", "line": 42, "msg": "; expected"}]}`
4.  Response: "Compilation failed. There is a syntax error in PlayerController.cs at line 42: '; expected'. Shall I fix it?"

## Best Practices
- Follow the patterns and constraints documented in this skill.
- Always run @context-discovery-agent before applying this skill to verify environment compatibility.
- Apply TDD where applicable: write the interface contract first, then implement.
- Zero GC in hot paths: cache references, avoid LINQ and 
ew allocations in Update loops.


---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void UnityBuildCommander_Should{ExpectedBehavior}_When{Condition}()
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
public void UnityBuildCommander_ShouldHandle{EdgeCase}()
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
public void UnityBuildCommander_ShouldThrow_When{InvalidInput}()
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
- @context-discovery-agent - Verify Unity version and package compatibility before proceeding
- @unified-style-guide - Naming and formatting conventions
- @automated-unit-testing - TDD scaffolding for this skill's components