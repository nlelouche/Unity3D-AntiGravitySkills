# 🌌 AntiGravity Skills
> *The "Cortex" for AI-Native Unity Development.*

![Unity](https://img.shields.io/badge/Unity-2023%2B-black?logo=unity)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)
![Skills](https://img.shields.io/badge/Skills-61_Active-purple)
![Templates](https://img.shields.io/badge/Templates-96_Ready-orange)

---

## 👋 Welcome to the Future of Game Dev
**AntiGravity Skills** is not just a code library—it's a **Standardized Knowledge Graph** designed to bridge the gap between Human creativity and AI execution.

*   **For AI Agents (Gemini, Copilot, Cursor)**: This repository acts as your **Long-Term Memory** and **Senior Tech Lead**. It provides context, architecture patterns, and "Do not hallucinate" constraints.
*   **For Human Developers**: This is a battle-tested modular framework. Need a system? Don't write it from scratch; invoke it.

---

## 🧩 What is a "Skill"?
In the context of Autonomous AI Agents, a **Skill** is a packaged unit of capability that bridges the gap between general reasoning and domain-specific execution.

Just as a human engineer might consult a technical manual or a senior mentor, an AI Agent "equips" a Skill to gain:
1.  **Procedural Knowledge**: Step-by-step workflows on *how* to solve a specific problem.
2.  **Contextual Awareness**: Constraints and rules (e.g., "Always use `StringBuilder` here") to prevent common pitfalls.
3.  **Tools & Templates**: Pre-verified code assets that ensure the output is production-ready, not just confident-sounding.

For a deep dive into the Skills architecture and protocol, consult the **[Official AntiGravity Documentation](https://antigravity.google/docs/skills)**.

---

## 🚀 Why AntiGravity?

### 🧠 Features for AI Agents
*   **Context Injection**: Stop guessing. Read `SKILL.md` files to understand the *exact* architecture requested before writing a single line of code.
*   **Zero-Shot Accuracy**: Use provided `templates/` to implement complex systems (FSMs, Inventory, Netcode) correctly on the first try.
*   **Standardization**: Every script follows specific namespaces, formatting, and patterns (SOLID, dependency injection), ensuring new code fits perfectly with existing code.

### 👤 Benefits for Humans
*   **Plug-and-Play Architecture**: Need a "Third Person Camera"? Invoke `@cinemachine-specialist`. Need "Inventory"? Invoke `@inventory-crafting-logic`.
*   **Production Standards**: From "Greybox" to "Gold Master", the skills cover every phase of production including DevOps, Analytics, and Optimization.
*   **Reduced Debt**: Code generated via these skills is pre-architected to be decoupled and testable.

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
├── 04-devops-automation/     # CI/CD, Build Pipelines
├── 05-ui-ux/                 # MVVM UI, Toolkits, HUDs
├── 06-performance/           # Optimization, Memory, Object Pooling
├── 07-tools-pipeline/        # Editor Tools, Asset Import, Git
├── 08-backend-monetization/  # Analytics, IAP, Multiplayer
└── 00-meta-skills/           # Agent Self-Replication & Leadership Tools
```

### Anatomy of a Skill
Every skill follows the **"Convergence Standard"**:
1.  **`SKILL.md`**: The brain. Contains the "When to Use", "Architecture Diagrams", and "Few-Shot Prompting Examples".
2.  **`templates/`**: C# scripts, Shaders, or Configs that are 90% complete and ready to deploy.
3.  **`examples/`**: (Optional) Reference scenes or usage examples.

---

## 🏛️ The Skill Catalog (The 12 Pillars)

### 1. Core Engineering (`00-core`)
*   **`unified-style-guide`**: The law of the land for C# formatting.

### 2. Architecture (`01-architecture`)
*   **`service-locator-pattern`**: Decoupled systems management.
*   **`event-bus-system`**: Global messaging without dependencies.
*   **`finite-state-machine`**: Robust AI and Player states.
*   **`save-load-serialization`**: JSON/Binary persistence encryption.
*   **`asynchronous-programming`**: UniTask and Coroutine management.

### 3. Gameplay (`02-gameplay`)
*   **`player-movement-controller`**: Kinematic and Physics-based movers.
*   **`camera-system-pro`**: Cinemachine orchestration.
*   **`universal-input-handler`**: New Input System wrapper.
*   **`combat-hitbox-system`**: Reliable damage detection.

### 4. Survival & Strategy (`03-survival-city-builder`)
*   **`grid-based-building-system`**: Placement logic for city builders.
*   **`resource-management-system`**: Inventory and economy.
*   **`horde-wave-logic`**: Spawners for tower defense/survival.
*   **`environment-hazard-system`**: Temperature, hunger, and thirst.

### 5. Visuals & Audio (`04-visuals-audio`)
*   **`shader-graph-master`**: Material templates.
*   **`particle-system-pro`**: VFX implementation.
*   **`audio-soundscape-architect`**: Mixer management and spatial audio.
*   **`lighting-nav-baker`**: Automation for Lightmapping and NavMesh.

### 6. DevOps & Automation (`04-devops`)
*   **`build-pipeline-manager`**: Headless CLI builds for CI/CD.

### 7. UI/UX (`05-ui-ux`)
*   **`ui-toolkit-modern`**: USS/UXML workflows.
*   **`mvvm-pattern`**: Model-View-ViewModel binding.
*   **`responsive-ui`**: Multi-resolution support.

### 8. Performance (`06-performance`)
*   **`object-pooling-system`**: Zero-alloc spawning.
*   **`addressables-asset-management`**: Async loading and memory care.
*   **`memory-profiler-expert`**: Leak detection.

### 9. Tools & Pipeline (`07-tools-pipeline`)
*   **`asset-import-pipeline`**: Auto-compress textures/models on import.
*   **`custom-editor-scripting`**: Inspector tools and windows.
*   **`automated-unit-testing`**: NUnit (EditMode & PlayMode) templates.
*   **`version-control-git`**: `.gitignore` and LFS automation.

### 10. Backend & Monetization (`08-backend`)
*   **`analytics-heatmaps`**: Telemetry tracking.
*   **`monetization-iap`**: Unity Purchasing wrapper.
*   **`backend-integration`**: Cloud save and login (PlayFab/Firebase).
*   **`multiplayer-netcode`**: NGO (Netcode for GameObjects) setup.

### 11. Meta Skills (`00-meta`)
*   **`skill-creator`**: Tools for creating new skills.
*   **`project-scaffolder`**: Initial folder generation.
*   **`virtual-production-lead`**: AI Director that reads GDDs and plans roadmaps.

---

## 🛠️ Workflow: How to use

### FOR AGENTS (The Loop)
1.  **Analyze**: User asks for a feature (e.g., "Make a wave spawner").
2.  **Search**: Look into `.agent/skills/`. Find `@horde-wave-logic`.
3.  **Read**: Consume `SKILL.md` to learn the architecture.
4.  **Implement**: Use `templates/WaveSpawner.cs.txt` as the base.
5.  **Refine**: Adapt the template to the user's specific requirements.

### FOR HUMANS (Installation)
Clone this repository into your project's root or as a submodule:

```bash
git clone https://github.com/YourOrg/AntiGravitySkills.git .agent/skills
```

Or run the setup script to bootstrap a new workspace:

```powershell
# Windows
.\Initialize.ps1
```

```bash
# Mac/Linux
./setup.sh
```

---

## 📊 Repository Stats

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
| DevOps & Pipeline | 4 | 4 |
| Core/Meta/Lead | 3 | 5 |
| **GRAND TOTAL** | **61** | **96** |

---

**AntiGravity Skills** — *Where Code Meets Intelligence.*
