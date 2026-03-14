---
name: dialogue-quest-system
description: "Complete dialogue and quest system with branching conversations, quest stages, and event triggers."
version: 2.0.0
tags: ["gameplay", "dialogue", "quests", "NPCs", "narrative"]
argument-hint: "action='create_quest' name='Kill10Rats' stages='Accept,InProgress,Complete'"
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
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
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



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void DialogueQuestSystem_Should{ExpectedBehavior}_When{Condition}()
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
public void DialogueQuestSystem_ShouldHandle{EdgeCase}()
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
public void DialogueQuestSystem_ShouldThrow_When{InvalidInput}()
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
- `@save-load-serialization` - Persist quest progress
- `@inventory-crafting-logic` - Quest rewards
- `@scriptableobject-architecture` - Data patterns

## Template Files
Available in templates/ folder.
