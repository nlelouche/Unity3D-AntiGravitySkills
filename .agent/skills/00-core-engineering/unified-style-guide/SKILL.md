---
name: unified-style-guide
description: Enforces a unified C# coding style and generates .editorconfig files. Use this to "fix formatting", "install style guide", or "check conventions".
argument-hint: "action='install' project_root='.'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# Unified Style Guide

## Goal
To maintain a consistent codebase by enforcing a standard `.editorconfig` across the project. This prevents "tab vs space" wars and ensures generated code matches the project's style.

## Rules
- **Naming**: Interfaces start with `I`, Private fields start with `_`.
- **Braces**: Allman style (New line before open brace).
- **Serialization**: `[SerializeField] private` is preferred over `public`.

## Procedure

1.  **Analyze Request**: Does the user want to *apply* the style or *check* it?
2.  **Execute Script**:
    - To Install: `python .../style_enforcer.py --action install`
    - To Check: `python .../style_enforcer.py --action check`
3.  **Report**: Confirm that the style guide is active.

## Few-Shot Example
User: "Set up the coding standards."
Agent: Runs `python style_enforcer.py --action install`
Output: "Success: Style guide installed."
Response: "I have configured the project with the standard .editorconfig rules."
