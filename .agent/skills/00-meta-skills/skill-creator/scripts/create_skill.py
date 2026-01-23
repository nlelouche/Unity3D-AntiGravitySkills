import argparse
import os
import sys

def create_skill(name, category, description):
    """
    Creates a new Production-Grade Skill structure.
    """
    # 1. Define Paths (assuming strict .agent/skills root relative to CWD)
    # We assume the script is run from the workspace root or we find the root.
    base_path = os.path.join(".agent", "skills")
    
    # Check if .agent/skills exists, if not, try to look relative to this script
    if not os.path.exists(base_path):
        # Fallback for testing: maybe we are running from inside .agent/skills
        # But for the agent environment, running from root is standard.
        print(f"Error: Could not find '{base_path}'. Please run this script from the workspace root.")
        sys.exit(1)

    category_path = os.path.join(base_path, category)
    skill_path = os.path.join(category_path, name)
    scripts_path = os.path.join(skill_path, "scripts")
    refs_path = os.path.join(skill_path, "references")
    assets_path = os.path.join(skill_path, "assets")

    # 2. Create Directories
    try:
        os.makedirs(scripts_path, exist_ok=True)
        os.makedirs(refs_path, exist_ok=True)
        os.makedirs(assets_path, exist_ok=True)
        print(f"Created directory structure at: {skill_path}")
    except OSError as e:
        print(f"Error creating directories: {e}")
        sys.exit(1)

    # 3. Generate SKILL.md
    skill_md_content = f"""---
name: {name}
description: {description}
argument-hint: "arg1='value' arg2='value'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
---

# {name.replace('-', ' ').title()}

## Goal
{description}

## Constraints
- Run safely and do not modify files without confirmation.
- Use the python scripts in `scripts/` for complex logic.

## Procedure
1.  **Analyze Request**: Understand what the user wants.
2.  **Execute Script**: Call the python script using `run_command`.
    - Command: `python .agent/skills/{category}/{name}/scripts/main.py --arg value`
3.  **Report**: Show the results to the user.

## Few-Shot Example
User: "Run {name}..."
Agent: execute python script...
"""
    
    with open(os.path.join(skill_path, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md_content)
    print("Generated SKILL.md")

    # 4. Generate Boilerplate Python Script (main.py)
    python_boilerplate = f"""import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--example_arg", help="An example argument", required=False)
    args = parser.parse_args()

    # Logic goes here
    print(f"Running skill '{name}'...")
    print(f"Example arg received: {{args.example_arg}}")

    # TODO: Implement core logic
    
    # Return 0 for success
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""

    with open(os.path.join(scripts_path, "main.py"), "w", encoding="utf-8") as f:
        f.write(python_boilerplate)
    print("Generated scripts/main.py")

    # 5. Generate requirements.txt
    with open(os.path.join(scripts_path, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write("# Add python dependencies here\n")
    print("Generated scripts/requirements.txt")

    print(f"SUCCESS: Skill '{name}' created successfully in category '{category}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap a new Antigravity Skill")
    parser.add_argument("--name", required=True, help="Kebab-case name of the skill")
    parser.add_argument("--category", required=True, help="Category folder (e.g., 01-architecture)")
    parser.add_argument("--description", required=True, help="Short description of the skill")
    
    args = parser.parse_args()
    
    create_skill(args.name, args.category, args.description)
