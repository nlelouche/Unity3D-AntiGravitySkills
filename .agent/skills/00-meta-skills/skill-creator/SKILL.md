---
name: skill-creator
description: Generates a new Production-Grade Skill (PG-Skill) with the correct folder structure and boilerplate files. Use this when the user asks to "create a new skill" or "bootstrap a skill".
argument-hint: "skill_name='my-new-skill' category='01-architecture' description='What does it do?'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - write_to_file
  - list_dir
---

# Skill Creator: The Meta-Agent Factory

## Goal
To bootstrap a new "Production-Grade Skill" folder structure that strictly adheres to the "Architecture Convergence" research paper standards. This ensures every new skill has a dedicated `scripts/` folder for Python logic and a standardized `SKILL.md`.

## Constraints & Rules
- **Naming Convention**: Skill names must be `kebab-case` (e.g., `unity-build-commander`).
- **Structure Enforcement**: You MUST NOT create just a `SKILL.md`. You MUST create the full folder hierarchy:
  ```text
  category/skill-name/
  ├── SKILL.md
  ├── scripts/
  │   ├── main.py
  │   └── requirements.txt
  ├── references/
  └── assets/
  ```
- **Python-First**: Always assume the skill will need a Python script. Generate a boilerplate `main.py` that handles argument parsing and logging.
- **YAML Frontmatter**: The `SKILL.md` must have valid YAML frontmatter including `name`, `description`, `argument-hint`, and `allowed-tools`.

## Procedure

1.  **Validate Input**: Ensure you have a `skill_name`, a `category` (folder name), and a `description`. If the category doesn't exist, suggest creating it or using a standard one.
2.  **Execute Generation Script**: The actual file creation logic is encapsulated in `scripts/create_skill.py`. This ensures consistency. Use `run_command` to execute this script.
    - Command: `python .agent/skills/00-meta-skills/skill-creator/scripts/create_skill.py --name "{skill_name}" --category "{category}" --description "{description}"`
3.  **Verify Output**: Check if the folder was created using `list_dir`.
4.  **Report to User**: Confirm the creation and provide the path to the new skill.

## Few-Shot Example

**User**: "Create a skill called 'asset-auditor' in '03-technical-art' to find large textures."

**Agent**:
1.  Identifies params: `name='asset-auditor'`, `category='03-technical-art'`, `desc='Finds large textures'`.
2.  Runs command: `python .agent/skills/00-meta-skills/skill-creator/scripts/create_skill.py --name "asset-auditor" --category "03-technical-art" --description "Finds large textures"`
3.  Output: "Skill created at .agent/skills/03-technical-art/asset-auditor"

## Python Script Wrapper
The python script `create_skill.py` handles the file I/O safely and populates the `SKILL.md` with the description provided.
