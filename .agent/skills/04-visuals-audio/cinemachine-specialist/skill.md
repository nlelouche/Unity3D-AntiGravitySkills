---
name: cinemachine-specialist
description: Setup helper for Cinemachine Virtual Cameras. Use to "make camera follow player", "screen shake setup", or "cutscenes".
argument-hint: "action='setup_follow' target='Player'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
  - mcp_unityMCP_manage_components
---

# Cinemachine Specialist

## Goal
To automate the potentially complex setup of Cinemachine Virtual Cameras (VCam).

## Strategy
Since Cinemachine is Component-heavy and not Script-heavy, this skill focuses on **Instructions** and **MCP Automation**.

## Procedure
1.  **Check**: Is the `CinemachineBrain` on the Main Camera?
2.  **Action**: Create a new GameObject "CM vcam1".
3.  **Component**: Add `CinemachineVirtualCamera`.
4.  **Config**: Set `Follow` and `LookAt` targets.

## MCP Integration
If MCP is active, this skill can use `manage_gameobject` to instantiate the VCam directly in the scene.
