---
name: procedural-animation-ik
description: Generates IK logic for feet, hands, and heads. Use for "realistic walking", "aiming at target", or "head look".
argument-hint: "name='FootIK' namespace='Game.Animation'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Procedural Animation (IK)

## Goal
To make characters interact physically with the world, avoiding the "floating feet" syndrome.

## Techniques
- **Foot IK**: Raycast down from feet to find ground point and adjust Animator bones.
- **Head Look**: Use `SetLookAtPosition` to track interesting objects.

## Procedure
1.  **Generate Script**: `FootIK.cs`.
2.  **Instruction**: Ensure the Animator Controller has "IK Pass" enabled in the Layer settings.

## Few-Shot Example
User: "Fix floating feet on uneven ground."
Agent: Generates `FootIK.cs`. "Attach this to your character and assign the Ground Layer."
