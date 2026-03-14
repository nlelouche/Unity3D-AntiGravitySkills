---
name: skill-creator
description: "Meta-skill for generating new Production-Grade Skills. Ensures consistency across the AntiGravity library by scaffolding folders and files."
version: 2.0.0
tags: ["meta", "scaffolding", "automation", "standards"]
argument-hint: "name='new-skill' category='01-architecture' description='Short goal'"
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

# Skill Creator (Meta)

## Overview
The "Factory" for all other skills. This meta-skill automates the creation of new skills to ensure they adhere to the **AntiGravity Professional Standard**. It scaffolds the directory structure, creates a robust `SKILL.md` from a template, and generates `scripts/` or `templates/` folders as needed.

## When to Use
- Use when **creating a new skill** from scratch.
- Use when **standardizing** an existing legacy skill.
- Use when bootstrapping a new category.
- Use to ensure **Architecture Convergence** across the agent's brain.

## Architecture

The Generator creates the following structure:

```text
.agent/skills/{category}/{skill-name}/
├── SKILL.md                 # The Brain (YAML + Markdown)
├── templates/               # C# / Shader / Text templates
│   └── MyTemplate.cs.txt
├── scripts/                 # (Optional) Python automation
│   └── main.py
└── references/              # (Optional) Documentation/Images
```

## Best Practices
- ✅ **Kebab-Case**: Always use `kebab-case` for skill names (e.g., `inventory-system`, not `InventorySystem`).
- ✅ **Categorization**: Place skills in the correct numbered category (e.g., `01-architecture`, `02-gameplay`).
- ✅ **Clean Description**: The YAML description should be actionable and concise.
- ✅ **Tags**: Add relevant tags for better semantic search.

## Procedure (Python Automation)

If Python is available, use the existing script to generate the skill.

1.  **Analyze Request**: Identify `name`, `category`, and `description`.
2.  **Execute Script**:
    ```bash
    python .agent/skills/00-meta-skills/skill-creator/scripts/create_skill.py --name "my-skill" --category "01-architecture" --description "My skill description"
    ```
3.  **Verify**: Check that `SKILL.md` exists and has the correct frontmatter.

## Manual Procedure (Fallback)

If Python is unavailable, use the **Reference Template** below to manually write the `SKILL.md`.

1.  Create usage folder: `.agent/skills/{category}/{name}/`
2.  Create `SKILL.md` using the **Professional Template** consistency.
3.  Fill in `Overview`, `When to Use`, `Architecture`, `Best Practices`, and `Few-Shot Examples`.



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void SkillCreator_Should{ExpectedBehavior}_When{Condition}()
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
public void SkillCreator_ShouldHandle{EdgeCase}()
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
public void SkillCreator_ShouldThrow_When{InvalidInput}()
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
- `@unified-style-guide` - Ensures code templates follow C# standards.
- `@version-control-git` - Commit the new skill immediately.
