---
name: unity-mcp-connector
description: Checks if the Unity Editor is connected via MCP and exposes runtime capabilities. Use to "check editor status", "find selected object", or "list scene objects".
argument-hint: "action='check_connection'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - mcp_unityMCP_manage_editor
  - mcp_unityMCP_find_gameobjects
  - mcp_unityMCP_manage_scene
  - run_command
  - list_dir
---

# Unity MCP Connector

## Goal
To serve as the **Bridge** between the Agent's file-system view and the running Unity Editor. It enables "Scene Awareness".

## Capabilities
1.  **Health Check**: Verifies if `unityMCP` server is responding.
2.  **Selection Access**: Gets the currently selected GameObject in the Editor (crucial for "Add script to *this* object" workflows).
3.  **Hierarchy Scanning**: Finds objects by name/tag to validate references.

## Procedure

### Scenario A: Check Connection
1.  **Action**: Call `mcp_unityMCP_manage_editor` with `action='telemetry_ping'`.
2.  **Result**:
    - **Success**: "Unity Editor is Connected (Version 2022.3...)".
    - **Failure**: "Unity Editor is NOT connected. Falling back to File System mode."

### Scenario B: Contextual Operation
**User**: "Create a script for the selected object."
1.  **Check**: `unity-mcp-connector` -> `editor_selection`.
2.  **Logic**:
    - If Object is "Player": Agent assumes `PlayerController`.
    - If Object is "MainCamera": Agent assumes `CameraFollow`.
3.  **Handoff**: Pass this context to `dots-system-architect` or `oop-patterns-architect`.

## Hybrid Rules
- **Non-Blocking**: Failure to connect via MCP should NEVER stop the agent. It must degrade gracefully to asking the user for the file path.
- **Read-Only Safety**: Prefer reading state (`get_active_scene`, `find_gameobjects`) over modifying state (`delete_gameobject`) unless explicitly commanded.
