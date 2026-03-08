---
name: unity-mcp-connector
description: "Orchestration bridge between AI Agents and the running Unity Editor instance via MCP (Model Context Protocol)."
version: 2.0.0
tags: ["mcp", "integration", "editor-api", "automation", "bridge"]
argument-hint: "action='ping' OR target='selection' scope='scene'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - mcp_unityMCP_manage_editor
  - mcp_unityMCP_find_gameobjects
  - mcp_unityMCP_manage_scene
  - mcp_unityMCP_manage_components
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
  gc_alloc_per_frame: "0 bytes target in hot paths"
  max_update_cost: "O(n) - profiler-guided"
tdd_first: false
---

# Unity MCP Connector

## Overview
Connects the file-based AI Brain with the live Unity Editor state. Allows the agent to "see" the scene hierarchy, inspect selected objects, and validate the existence of components dynamically.

## When to Use
- Use to check if Unity Editor is open and listening
- Use to find the currently selected GameObject context
- Use to validate scene contents that aren't serialized to disk yet
- Use to trigger Editor actions (Play, Pause, Refresh)
- Use to read console logs for errors

## Capabilities

| Capability | Tool | Description |
|------------|------|-------------|
| **Telemetry** | `manage_editor` | Check connection health (Ping) |
| **Selection** | `manage_editor` | Get/Set user selection |
| **Hierarchy** | `find_gameobjects` | Search active scene objects |
| **State** | `manage_editor` | Play/Pause/Stop mode control |
| **Scene** | `manage_scene` | Open/Save scenes |

## Procedure

### 1. Connection Check (First Step)
Always verify the bridge is active before attempting complex operations.
```json
{
  "tool": "mcp_unityMCP_manage_editor",
  "args": { "action": "telemetry_ping" }
}
```

### 2. Context Retrieval
If the user says "Add script to **this** object", fetch the selection.
```json
{
  "tool": "mcp_unityMCP_manage_editor",
  "args": { "action": "get_selection" } // (Hypothetical param, usually implied or via finding)
}
```
*Note: Currently `telemetry_status` or specific find commands might be needed depending on server implementation.*

### 3. Graceful Fallback
If MCP tools fails or returns "Not Connected":
1. **Log**: "Unity Editor not reachable. Proceeding in File-System Mode."
2. **Ask**: "Please specify the file path or GameObject name manually."
3. **Continue**: Do not halt the workflow.

## Best Practices
- ✅ **Ping First**: Always check `telemetry_ping` before deep operations.
- ✅ **Read-Only Default**: Prefer reading state to modifying state unless explicitly requested.
- ✅ **Error Handling**: Catch tool failures gracefully (Editor might be compiling).
- ❌ **NEVER** assume Editor is open.
- ❌ **NEVER** rely solely on MCP for critical data (File System is truth).

## Few-Shot Examples

### Example 1: Check Status
**User**: "Is Unity connected?"

**Agent**:
```javascript
// Calls mcp_unityMCP_manage_editor with action='telemetry_ping'
// Output: "pong"
// Response: "Yes, Unity Editor is connected and responding."
```

### Example 2: Find Player
**User**: "Where is the player in the scene?"

**Agent**:
```javascript
// Calls mcp_unityMCP_find_gameobjects with search_term='Player'
// Output: [{ name: "Player", id: 1234, ... }]
// Response: "Found 'Player' with InstanceID 1234."
```

## Related Skills
- `@custom-editor-scripting` - Build tools utilizing this connection
- `@automated-unit-testing` - Trigger tests via MCP
