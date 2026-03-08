# 🌌 AntiGravity Skills
> *The "Cortex" for AI-Native Unity Development — 2026 Edition.*

[![Leer en Español](https://img.shields.io/badge/Leer%20en-Español-red)](README.es.md)
![Unity](https://img.shields.io/badge/Unity-6%2B-black?logo=unity)
![CSharp](https://img.shields.io/badge/C%23-12-purple?logo=csharp)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)
![Skills](https://img.shields.io/badge/Skills-84_Active-purple)
![Standard](https://img.shields.io/badge/Standard-2026%20Edition-gold)
![PeerReview](https://img.shields.io/badge/Peer%20Review-Validated-brightgreen)

---

## 👋 Welcome to the Future of Game Dev
**AntiGravity Skills** is not just a code library — it's a **Standardized Knowledge Graph** designed to bridge the gap between Human creativity and AI execution. Every skill is a portable, self-contained intelligence unit: agnostic to genre, platform, and project.

*   **For AI Agents (Gemini, Copilot, Cursor)**: Long-term memory + Senior Tech Lead. Provides context, architecture patterns, and "Do not hallucinate" constraints via the **2026 Tier Architecture**.
*   **For Human Developers**: A battle-tested modular framework. Need a system? Don't write it from scratch — invoke it.

> [!IMPORTANT]
> **🤖 Enables the "Tech Lead" Persona**
> Loading `AGENT.md` activates the **AntiGravity Architect** persona. The agent acts as a **Senior Mentor** — explaining SOLID patterns, warning about GC pressure, and enforcing the **2026 TDD-First protocol** while it builds.

---

## 🧩 What is a Skill?
A **Skill** is a packaged unit of capability that bridges general reasoning with domain-specific execution. When an AI Agent reads a `SKILL.md`, it gains:

1.  **Procedural Knowledge**: Step-by-step workflows for specific problems.
2.  **Contextual Awareness**: Rules and constraints to prevent common Unity pitfalls.
3.  **Templates**: Pre-verified C# code ready for production.

---

## 🆕 2026 Standard — What Changed

| Feature | Before | 2026 Edition |
|---------|--------|-------------|
| **Unity Target** | 2023+ | **Unity 6+ / CoreCLR** |
| **Language** | C#10 | **C#12 with Span\<T\>** |
| **Pre-flight** | Manual | **Context Discovery Protocol** |
| **Testing** | Optional | **TDD-First (Mandatory)** |
| **GC Policy** | Guidelines | **Zero GC in hot paths** |
| **Skill Metadata** | Name + tags | **Full YAML: requirements, tiers, budgets** |

> [!NOTE]
> All **84 skills** now carry full 2026-standard YAML metadata (`requirements`, `context_discovery`, `performance_budget`, `tdd_first`). 20 new skills are TDD-First native. The 64 legacy skills are tagged **`tdd_first: false`** and marked *"Legacy — Refactor Pending"* — this is an honest signal, not a defect. See [Roadmap](#-roadmap--v21-next-skills) for the upgrade plan.

---

## 🏗️ System Architecture

```text
.agent/skills/
├── 00-core-engineering/      # C#12, GC Watchdog, Style Guide
├── 01-architecture/          # Service Locator, Repository, Command, FSM, Events
├── 02-gameplay/              # Combat, Camera, Minimap, Replay, Procedural Gen
├── 03-simulation-strategy/   # Grid Building, Resources, Waves  [Agnostic 2026]
├── 04-visuals-audio/         # Shaders, VFX, Lighting, Audio
├── 05-ui-ux/                 # MVVM, UI Toolkit, Accessibility (WCAG 2.1)
├── 06-performance/           # Job System, GPU Instancing, Texture Streaming
├── 07-tools-pipeline/        # Context Discovery, AI Code Reviewer, Validator
├── 08-backend-monetization/  # PlayFab Economy v2, UGS, Ads Mediation
├── 09-devops-automation/     # CI/CD, Build Pipelines
└── 00-meta-skills/           # Skill Creator, Project Scaffolder
```

### 2026 Tier Architecture

Every skill operates on 3 tiers, optimized for AI consumption:

| Tier | Content | Consumed by |
|------|---------|------------|
| **Tier 1** | YAML frontmatter (requirements, context_discovery, performance_budget) | Machine — **hard-blocking gate** |
| **Tier 2** | SKILL.md body (When to Use, Architecture, Code Examples) | AI reasoning |
| **Tier 3** | `templates/` directory (C# files) | Direct code injection |

> [!IMPORTANT]
> **Tier 1 is a hard-blocking gate.** If `requirements.unity_version` or `render_pipeline` don't match the project's `ContextReport`, the agent must stop and report the incompatibility before writing any code. Proceeding without meeting requirements requires an explicit user `--force` override, which the agent must log visibly.

---

## 🏛️ Skill Catalog (84 Active Skills)

### ⚙️ Core Engineering (`00-core-engineering`)
*   **`unified-style-guide`** — C#12, CoreCLR, Zero GC rules
*   **`unity-compile-fixer`** ⭐ NEW — Agentic C# error repair loop
*   **`coreclr-gc-watchdog`** ⭐ NEW — GC pressure classification + zero-alloc patterns
*   **`csharp12-features-guide`** ⭐ NEW — Safety matrix for C#12 features in Unity 6

### 🏛 Architecture (`01-architecture`)
*   **`service-locator-pattern`** ⭐ NEW — Type-safe SL with DI decision matrix
*   **`repository-pattern`** ⭐ NEW — Generic `IRepository<T>` with async I/O + mock
*   **`command-pattern-undo`** ⭐ NEW — Undo/Redo history stack
*   **`event-bus-system`**, **`finite-state-machine`**, **`save-load-serialization`**, **`asynchronous-programming`**

### 🎮 Gameplay (`02-gameplay`)
*   **`procedural-generation`** ⭐ NEW — BSP Dungeon + Perlin Terrain with `IGrid<T>`
*   **`replay-system`** ⭐ NEW — Deterministic input recording + death-cam
*   **`minimap-system`** ⭐ NEW — Orthographic RenderTexture minimap with icon layers
*   **`player-movement-controller`**, **`camera-system-pro`**, **`combat-hitbox-system`**

### 🎯 Simulation & Strategy (`03-simulation-strategy`)
*   **`grid-based-building-system`**, **`resource-management-system`**, **`horde-wave-logic`**, **`environment-hazard-system`**

### 🎨 Visuals & Audio (`04-visuals-audio`)
*   **`shader-graph-expert`**, **`vfx-graph-shuriken`**, **`dynamic-audio-mixers`**, **`lighting-nav-baker`**

### 🖥️ UI/UX (`05-ui-ux`)
*   **`mvvm-binding-system`** ⭐ NEW — Full MVVM for UI Toolkit with `[CreateProperty]`
*   **`accessibility-hci`** ⭐ NEW — WCAG 2.1, colorblind shaders, control remapping
*   **`canvas-performance`**, **`responsive-ui-design`**, **`input-system-new`**

### ⚡ Performance (`06-performance`)
*   **`job-system-burst`** ⭐ NEW — Unity Jobs + Burst Compiler (0 GC, parallel CPU)
*   **`gpu-instancing-expert`** ⭐ NEW — `DrawMeshInstancedIndirect`, 100k meshes/draw call
*   **`texture-streaming-expert`** ⭐ NEW — Mip Streaming budget + `TextureAuditTool`
*   **`object-pooling-system`**, **`addressables-asset-management`**, **`memory-profiler-expert`**

### 🛠️ Tools & Pipeline (`07-tools-pipeline`)
*   **`context-discovery-agent`** ⭐ NEW — Auto-detects Unity version, RP, packages → ContextReport
*   **`ai-code-reviewer`** ⭐ NEW — CRITICAL/WARNING/INFO code review checklist
*   **`metadata-validator`** ⭐ NEW — Compliance audit script for all SKILL.md files
*   **`automated-unit-testing`**, **`custom-editor-scripting`**, **`version-control-git`**

### 💰 Backend & Monetization (`08-backend-monetization`)
*   **`playfab-economy-v2`** ⭐ NEW — Economy v2 API (deprecates v1), `IPlayFabEconomyService`
*   **`unity-gaming-services`** ⭐ NEW — UGS: Auth, Lobby, Relay, Leaderboards, Cloud Save
*   **`ads-mediation-ironsource`** ⭐ NEW — LevelPlay rewarded/interstitial + GDPR consent
*   **`analytics-heatmaps`**, **`monetization-iap`**, **`multiplayer-netcode`**

### 🚀 DevOps & Automation (`09-devops-automation`)
*   **`build-pipeline-manager`**, **`unity-build-commander`**

---

## 🏷️ Skill Quality Tags

Every skill carries a `tdd_first:` field that signals its quality level:

| Tag | Meaning | What to expect |
|-----|---------|----------------|
| `tdd_first: true` ⭐ | 2026 Native | Interface + failing test + implementation + mock. Production-grade. |
| `tdd_first: false` 🔧 | Legacy — Refactor Pending | Solid architecture, but no TDD scaffold. Use with extra review. |

> Honesty matters: the agent uses `tdd_first` to calibrate its review strictness. A `false` signals that the agent should be more critical of generated code, not more lenient.

---

## ⚡ 2026 Context Discovery Protocol

Before generating any code, the agent runs a **pre-flight check**:

```json
// Produced by @context-discovery-agent
{
  "unity_version": "6000.1.2f1",
  "render_pipeline": "URP",
  "awaitable_api": true,
  "burst_available": true,
  "packages": ["com.unity.inputsystem", "com.unity.services.core"]
}
```

This ensures every generated script is **compatible with your exact environment** — no more "this only works in HDRP" surprises.

---

## 🛠️ Workflow

### FOR AGENTS (The Loop)
1.  **Detect**: Run `@context-discovery-agent` → get `ContextReport`.
2.  **Find**: Locate the relevant skill in `.agent/skills/`.
3.  **Gate**: Check `requirements:` in YAML frontmatter against `ContextReport`.
4.  **Read**: Consume the SKILL.md body for architecture + patterns.
5.  **Implement**: Inject from `templates/`, adapt to project context.
6.  **Review**: Run `@ai-code-reviewer` before committing.

### 🧑‍💻 FOR HUMANS: Stop "Vibe Coding" Garbage

The biggest mistake developers make with AI tools (Copilot, Cursor, Gemini) is **"Vibe Coding"** — asking the AI to build systems without providing strict architectural boundaries. This results in spaghetti code, memory leaks, and unscalable games.

**AntiGravity Skills CLI** solves this by injecting production-ready, Senior-level patterns directly into your project.

#### Why use this?
*   **For Juniors:** Stop guessing how to build an Object Pool or an Event Bus. The CLI injects clean, heavily-commented, industry-standard C# code directly into your project for you to study and use.
*   **For Seniors & AI:** Every installed skill includes a `SKILL.md` file. When you ask your AI assistant to modify the injected code, it reads this file first. The strict rules inside prevent the AI from hallucinating or breaking the architecture.

#### How to use it (Zero Installation)
Thanks to `npx`, **no local installation or repo cloning is required**. The CLI checks your Unity version and Render Pipeline to prevent compatibility issues, then injects bare C# code ("Zero-Lock-In") directly into `Assets/Plugins/AntiGravitySkills/`.

Run this from your Unity project root:

```bash
# 1. Search the catalog for the system you need
npx github:nlelouche/Unity3D-AntiGravitySkills list

# 2. Check its requirements (Unity version, packages) before installing
npx github:nlelouche/Unity3D-AntiGravitySkills info event-bus-system

# 3. Inject the code safely into your project
npx github:nlelouche/Unity3D-AntiGravitySkills add event-bus-system
```

*Note for local AI Agents: You can still clone the full repo into `.agent/skills/` if you want your agent to have permanent offline access to the entire knowledge graph.*
```bash
git clone https://github.com/nlelouche/Unity3D-AntiGravitySkills.git .agent/skills
```

---

## 🗺️ Roadmap — v2.1 Next Skills

Based on architectural review and gap analysis, the following skills are prioritized for the next iteration:

| Priority | Skill | Category | Justification |
|----------|-------|----------|---------------|
| 🔴 High | `netcode-for-gameobjects` | `01-architecture` | Largest gap — only core Unity 6 system without coverage |
| 🔴 High | `localization-unity-package` | `07-tools-pipeline` | Complex `StringTable` + `LocalizeStringEvent` setup is a prime AI pain-point |
| 🟡 Medium | `xr-toolkit-vr` | `02-gameplay` | VR/MR market growth (Quest 3, Vision Pro) — platform-agnostic XR skill |
| 🟡 Medium | `dots-physics` | `06-performance` | Natural companion to `job-system-burst` for physics-heavy simulations |
| 🟢 Low | `websockets-native` | `08-backend-monetization` | Partially covered by UGS Relay — lower priority unless non-UGS projects |

---

## 📊 Repository Stats (2026 Edition)

| Category | Skills | TDD-Native |
|:---------|:------:|:----------:|
| Core Engineering | 4 | 3 |
| Meta Skills | 3 | 0 |
| Architecture | 13 | 3 |
| Gameplay | 14 | 3 |
| Simulation & Strategy | 6 | 0 |
| Visuals & Audio | 9 | 0 |
| UI/UX | 8 | 2 |
| Performance | 8 | 3 |
| Tools & Pipeline | 9 | 4 |
| Backend & Monetization | 8 | 3 |
| DevOps & Automation | 2 | 0 |
| **GRAND TOTAL** | **84** | **20** |

---

## 🗂️ CHANGELOG

See [CHANGELOG.md](CHANGELOG.md) for the full history.

---

**AntiGravity Skills** — *Where Code Meets Intelligence. 2026 Edition.*
