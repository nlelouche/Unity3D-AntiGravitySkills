# AntiGravity Unity Skills Ecosystem 🌌

Welcome to the **AntiGravity Agency Brain**.
This repository contains **52 Production-Grade Unity Skills** that transform a standard AI agent into an Expert Unity Game Developer.

---

## 🧠 How It Works

### Integration Strategy: The "Shared Brain" Model
We recommend treating this repository as a **Git Submodule** within your Unity projects. This architecture allows multiple game projects to share a single, evolving "Brain" of skills.

#### Installation (Git Submodule)
1. Run this command from your Unity project's root:
   ```bash
   # Adds AntiGravity as a tools submodule
   git submodule add https://github.com/YourOrg/AntiGravitySkills.git .agent/antigravity
   ```
2. **Run the Initialization Script** (One-time Setup):
   * **Windows**: Run `.\.agent\antigravity\Initialize.ps1`
   * **Mac/Linux**: Run `./.agent/antigravity/setup.sh`

   > **🛠️ What does this script do?**
   > *   **It does NOT move your files:** Your submodule integrity remains untouched.
   > *   **Symlinks the Brain (`.agent/skills`):** It creates a **Symbolic Link** (or Junction on Windows) from your project's `.agent/skills` folder to the submodule. This means if you update the submodule (`git submodule update`), your Agent immediately sees the new skills without you needing to copy anything.
   > *   **Copies the Persona (`AGENT.md`):** It duplicates `AGENT.md` to your project root. This is a **copy**, not a link, so you can customize the Agent's personality for *this specific project* (e.g., adding specific rules) without altering the shared codebase.

#### The Workflow
1.  **Project Specific**: Your game code lives in `Assets/`.
2.  **The Brain**: The agent reads strict architectural patterns from `.agent/antigravity/skills/`.
3.  **Updates**: When you improve a skill (e.g., better FPS controller), push changes to this repo.
    - Go to your other projects and run `git submodule update --remote` to inherit the upgrades instantly.

#### Contributing
This is an open "Knowledge Base".
- **Found a bug in a template?** Submit a Pull Request.
- **Created a new system?** Add a folder to `skills/` and submit a PR.
- **Goal**: To build the ultimate, community-driven Unity Agent memory.

### Integration with AntiGravity Agent
"AntiGravity" (the Agent) uses this folder structure as its **Long-Term Procedural Memory**.

1.  **Discovery**: When you ask for a task (e.g., "Create an Inventory"), the Agent scans the `SKILL.md` files in this repository.
2.  **Matching**: It looks at the **YAML Frontmatter** in each `SKILL.md` (specifically `description` and `argument-hint`) to find the best tool for the job.
3.  **Execution**: Once a skill is selected, the Agent reads the **Procedure** section and executes the associated Python scripts (`scripts/*.py`) or copies the C# Templates (`templates/*.txt`).

### The Structure of a Skill
Every skill follows this standardized architecture:

```text
category-name/
  └── skill-name/
      ├── SKILL.md          <-- The "Brain" (Instructions, Goals, Architecture)
      ├── templates/        <-- The "Body" (Raw C# code, TextAssets)
      └── scripts/          <-- The "Hands" (Python automation logic)
```

---

## 📚 Skill Inventory (51 Skills)

### I. Architecture & Core (`01-architecture`)
*Foundation for scalable codebases.*
- `dots-system-architect`: High-performance Data-Oriented Technology Stack.
- `di-container-manager`: Dependency Injection (VContainer/Zenject).
- `oop-patterns-architect`: FSM, Singleton, Observer implementations.
- `advanced-design-patterns`: Command, Strategy, Factory patterns.
- `scriptable-object-architecture`: Flexible data containers.
- `advanced-game-bootstrapper`: Persistent initialization scene pattern.

### II. Gameplay (`02-gameplay`)
*Mechanics and Interaction.*
- `advanced-character-controller`: Kinematic (FPS) & Rigidbody (Physics) movement.
- `ability-skill-system`: Data-driven spells and cooldowns.
- `inventory-crafting-logic`: MVC-based inventory management.
- `damage-health-framework`: IDamageable, Health, Death events.
- `status-effect-system`: Buffs, Debuffs, DOTs.
- `ai-behavior-trees`: Modular AI nodes (Selector, Sequence).
- `navmesh-pathfinding`: Agent navigation and obstacle avoidance.
- `loot-rng-management`: Weighted drop tables.
- `dialogue-quest-system`: Branching conversations.
- `save-load-serialization`: JSON persistence.
- `physics-logic`: Raycast and Overlap optimized wrappers.

### III. Survival & City Builder (`03-survival-city-builder`)
*Complex simulation systems.*
- `resource-management-system`: Economy (Wood, Gold, Stone).
- `grid-based-building-system`: Snapping and placement logic.
- `horde-wave-logic`: Spawning managers for Tower Defense.
- `tech-tree-research`: Unlockable upgrade graphs.
- `unit-population-ai`: Optimized crowd management.
- `environment-hazard-system`: Hunger, Thirst, Temperature.

### IV. Visuals & Audio (`04-visuals-audio`)
*Polish and Feedback.*
- `dynamic-audio-mixers`: Sound pooling and AudioMixer groups.
- `juice-game-feel`: Screen shake, hit stop, squash & stretch.
- `procedural-animation-ik`: Foot/Hand IK placement.
- `cinemachine-specialist`: Camera rigs and transitions.
- `shader-graph-expert`: Material manipulation helpers.
- `vfx-graph-shuriken`: Particle system management.
- `lighting-post-processing`: Render settings configuration.

### V. UI/UX (`05-ui-ux`)
*Interface and Control.*
- `ui-toolkit-architect`: UXML/USS document Logic.
- `input-system-new`: InputReader event bus wrapper.
- `menu-navigation-flow`: Stack-based UI history.
- `canvas-performance`: Optimization best practices.
- `responsive-ui-design`: Anchor and pivot helpers.

### VI. Optimization (`06-performance`)
*Performance tuning.*
- `object-pooling-system`: Generic GameObject recycling.
- `addressables-asset-management`: Async asset loading.
- `mobile-optimization`: Frame rate and battery settings.
- `memory-profiler-expert`: Texture and Heap tracking tools.
- `lod-occlusion-culling`: Rendering optimization setup.

### VII. Tools & Pipeline (`07-tools-pipeline`)
*Developer efficiency.*
- `custom-editor-scripting`: Custom Inspectors and Windows.
- `unity-build-commander`: CI/CD automation scripts.
- `automated-unit-testing`: NUnit test (PlayMode/EditMode) stubs.
- `localization-specialist`: String table management.
- `version-control-git`: .gitignore and LFS setup.
- `unity-mcp-connector`: Integration with Model Context Protocol.

### VIII. Backend (`08-backend-monetization`)
*Services and Revenue.*
- `service-layer-generator`: Backend API wrappers.
- `multiplayer-netcode`: NetworkManager (NGO) stubs.
- `monetization-iap`: Unity IAP wrappers.
- `analytics-heatmaps`: Event tracking setup.

---

## 🚀 Usage Guide

**To use a skill:**
Simply ask the Agent in natural language.
> "I need a character controller with a double jump."
> "Create a save system for my RPG."
> "Set up an inventory with wood and stone."

**To modify a skill:**
Edit the `templates/` files directly. The Agent will use your updated code in future generations.

---

*Generated by AntiGravity Agent.*
