---
name: unity-build-commander
description: Executes a headless Unity build for the target platform (Windows/Android/iOS), parses the Editor.log for compilation errors, and reports the build status. Use this when the user asks to "build the game" or "check for compile errors".
argument-hint: "target='StandaloneWindows64' build_path='Builds/Win64'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Unity Build Commander

## Goal
To autonomously execute a Unity build process via the CLI, capture the output logs, parse them for errors, and provide a definitive success/failure report. This allows the agent to verify its own code changes.

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
