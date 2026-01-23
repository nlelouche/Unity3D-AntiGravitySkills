---
name: dialogue-quest-system
description: "Complete dialogue and quest system with branching conversations, quest stages, and event triggers."
version: 1.0.0
tags: ["gameplay", "dialogue", "quests", "NPCs", "narrative"]
argument-hint: "action='create_quest' name='Kill10Rats' stages='Accept,InProgress,Complete'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Dialogue Quest System

## Overview
Complete dialogue and quest system with branching conversations, multiple quest stages, objectives, rewards, and event-driven progression.

## When to Use
- Use when implementing NPC conversations
- Use when creating branching dialogue
- Use when tracking quest progress
- Use when implementing objectives (kill X, collect Y)
- Use when rewarding quest completion

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DialogueSO                               │
├─────────────────────────────────────────────────────────────┤
│  DialogueNode[] (Speaker, Text, Choices)                    │
│  Conditions (RequiredQuest, MinLevel)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     QuestSO                                 │
├─────────────────────────────────────────────────────────────┤
│  Stages: NotStarted → InProgress → Completed                │
│  Objectives: [{Type, Target, Count}]                        │
│  Rewards: [Item, XP, Gold]                                  │
└─────────────────────────────────────────────────────────────┘
```

## Quest States
- **NotStarted**: Quest available but not accepted
- **InProgress**: Quest active, tracking objectives
- **Completed**: All objectives done, rewards pending
- **TurnedIn**: Rewards collected, quest finished
- **Failed**: Quest failed (optional)

## Objective Types
- **Kill**: Kill X enemies of type Y
- **Collect**: Obtain X items
- **Interact**: Talk to NPC, use object
- **Reach**: Arrive at location
- **Escort**: Keep NPC alive to destination

## Best Practices
- ✅ Use ScriptableObjects for dialogue/quest data
- ✅ Implement ISaveable for quest progress
- ✅ Use events for objective updates
- ✅ Support quest prerequisites
- ❌ **NEVER** hardcode dialogue text
- ❌ **NEVER** forget to save quest state

## Few-Shot Examples

### Example 1: Kill Quest
**User**: "Quest to kill 10 wolves."

**Agent**:
```csharp
// QuestSO asset with objective:
// Type: Kill, TargetId: "wolf", RequiredCount: 10
// Reward: 100 gold, 50 XP
```

### Example 2: Dialogue Choice
**User**: "NPC offers two quest paths."

**Agent**:
```csharp
DialogueNode choice = new()
{
    Speaker = "Elder",
    Text = "Which path will you take?",
    Choices = new[] 
    {
        { Text = "The Mountains", NextNode = mountainQuestNode },
        { Text = "The Forest", NextNode = forestQuestNode }
    }
};
```

## Related Skills
- `@save-load-serialization` - Persist quest progress
- `@inventory-crafting-logic` - Quest rewards
- `@scriptableobject-architecture` - Data patterns

## Template Files
Available in templates/ folder.
