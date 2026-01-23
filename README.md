# AntiGravity Skills 🌌
### The Ultimate AI-Native Unity Development Brain

![Unity](https://img.shields.io/badge/Unity-2023%2B-black)
![License](https://img.shields.io/badge/License-MIT-green)
![Skills](https://img.shields.io/badge/Skills-56_Active-blue)
![Templates](https://img.shields.io/badge/Templates-90_Ready-orange)

**AntiGravity Skills** is a standardized, modular library of "Skills" designed to empower AI Agents (like Gemini, Claude, Cursor) to act as **Senior Unity Engineers**. 

Each skill contains **Context**, **Architecture**, **Best Practices**, and **Production-Ready Templates**, enabling the AI to write robust, scalable, and industry-standard code without hallucinating or using deprecated APIs.

---

## 🏗️ System Architecture

The repository is structured for automatic ingestion by MCP-enabled agents.

```text
.agent/skills/
├── 00-core-engineering/      # Coding Standards & Style Guides
├── 01-architecture/          # Core Systems (Events, FSM, Save/Load)
├── 02-gameplay/              # Mechanics (Combat, Camera, Input)
├── 03-survival-city-builder/ # Genre: Survival & Strategy
├── 04-visuals-audio/         # Shaders, VFX, SFX
├── 05-ui-ux/                 # MVVM UI, Toolkits, HUDs
├── 06-performance/           # Optimization, Memory, Object Pooling
├── 07-tools-pipeline/        # Editor Tools, CI/CD, Git
├── 08-backend-monetization/  # Analytics, IAP, Multiplayer
└── 00-meta-skills/           # Agent Self-Replication Tools
```

### Anatomy of a Skill
Every skill follows the **"Convergence Standard"**:
1.  **`SKILL.md`**: The brain. Contains the "When to Use", "Architecture", and "Few-Shot Examples".
2.  **`templates/`**: C# scripts, Shaders, or Configs that are 90% complete and ready to deploy.
3.  **`scripts/`** (Optional): Python/Bash automation for complex tasks.

---

## 🏛️ The 10 Pillars of AntiGravity

### 1. Core Engineering (`00-core`)
Establishes the ground rules.
- **Skills**: `unified-style-guide`
- **Focus**: C# Coding Standards, .editorconfig, Code Reviews.

### 2. Architecture (`01-architecture`)
The backbone of scalable games.
- **Key Skills**: `service-locator-pattern`, `event-bus-system`, `finite-state-machine`, `save-load-serialization`, `asynchronous-programming`.
- **Philosophy**: ZERO tight coupling. Interface-driven design.

### 3. Gameplay (`02-gameplay`)
The "Fun" factor.
- **Key Skills**: `player-movement-controller`, `camera-system-pro`, `universal-input-handler`, `combat-hitbox-system`.
- **Philosophy**: Modular components over monoliths.

### 4. Survival & Strategy (`03-survival-city-builder`)
Specialized genre mechanics.
- **Key Skills**: `grid-based-building`, `resource-management`, `horde-wave-logic`, `environment-hazard-system`.

### 5. Visuals & Audio (`04-visuals-audio`)
The juice and feel.
- **Key Skills**: `shader-graph-master`, `particle-system-pro`, `audio-mixing-system`.

### 6. UI/UX (`05-ui-ux`)
Pixel-perfect interfaces.
- **Key Skills**: `ui-toolkit-modern`, `mvvm-pattern`, `tweening-animation`.

### 7. Performance (`06-performance`)
60 FPS on mobile.
- **Key Skills**: `object-pooling-system`, `addressables-asset-management`, `memory-profiler-expert`.

### 8. Tools & Pipeline (`07-tools-pipeline`)
Developer productivity.
- **Key Skills**: `custom-editor-scripting`, `automated-unit-testing`, `version-control-git`.

### 9. Backend & Monetization (`08-backend`)
LiveOps and Revenue.
- **Key Skills**: `analytics-heatmaps`, `monetization-iap`, `backend-integration`.

### 10. Meta Skills (`00-meta`)
The Agent's self-improvement toolset.
- **Skills**: `skill-creator` (The factory that builds this repo).

---

## 🚀 Quick Start

### For Users
To use these skills in your project, simply ask your AI Agent:
> "Initialize the AntiGravity library."

Or run the setup script manually:
```powershell
# Windows
.\Initialize.ps1
```
```bash
# Mac/Linux
./setup.sh
```

### For Agents
1.  **Audit**: Run `task_boundary` to define your goal.
2.  **Search**: Use `find_by_name` to locate relevant `SKILL.md` files.
3.  **Read**: Consume the `SKILL.md` to understand the architecture.
4.  **Implement**: Use the provided `templates/` to generate high-quality code.

---

## 📊 Project Statistics

| Category | Skills Authenticated | Templates Ready |
|:---------|:--------------------:|:---------------:|
| Architecture | 10 | 29 |
| Gameplay | 11 | 26 |
| Visuals & Audio | 8 | 10 |
| UI/UX | 5 | 5 |
| Survival/Strategy | 6 | 6 |
| Performance | 5 | 3 |
| Tools Breakdown | 5 | 4 |
| Backend Ops | 4 | 4 |
| Core/Meta | 2 | 3 |
| **TOTAL** | **56** | **90** |

---

## 🤝 Contributing

1.  **Fork** the repository.
2.  **Create a Skill**: Use the `skill-creator` meta-skill to generate the folder structure.
3.  **Template**: Add a `SKILL.md` and at least one C# `template`.
4.  **PR**: Submit your PR with the tag `[New Skill]`.

---

**AntiGravity Skills** — *Where Code Meets Intelligence.*
