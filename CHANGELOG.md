# CHANGELOG — AntiGravity Skills

All notable changes to the **AntiGravity Skills** repository are documented here.

Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`

---

## [2.0.0] — 2026-03-08 — *"The 2026 Edition"*

### 🎯 Highlights
- Targets **Unity 6+ / CoreCLR / C# 12** (upgraded from Unity 2023 / Mono / C#10)
- Introduces the **2026 Standard**: mandatory YAML frontmatter with `requirements`, `context_discovery`, `performance_budget`, and `tdd_first` blocks on all new skills
- **+20 new skills** across all categories — total grows from 64 → **84 active skills**
- Category `03-survival-city-builder` renamed to **`03-simulation-strategy`** for genre agnosticism

---

### ✨ Added — Foundation

#### `AGENT.md` — 2026 Edition
- §5 **Context Discovery Protocol**: Mandatory pre-flight reads `ProjectVersion.txt`, detects Render Pipeline, parses `manifest.json`
- §6 **Performance as Default**: Zero GC mandate, no `GetComponent` in loops, Interface-First, no LINQ in hot paths
- §7 **Tier Architecture**: Tier 1 (YAML) → Tier 2 (MD body) → Tier 3 (Templates) activation flow
- §8 **TDD-First Protocol**: Interface → Test RED → Implement GREEN → Refactor

#### `SKILL_MASTER_TEMPLATE.md` — New
- Canonical reference for all 2026-standard skills
- Defines all required YAML fields, Tier Architecture, and directory conventions

---

### ✨ Added — Batch A: Core New Skills (5 skills)

| Skill | Category | Key Feature |
|-------|---------|------------|
| `unity-compile-fixer` | `00-core-engineering` | Error Classification Map + surgical fix loop |
| `context-discovery-agent` | `07-tools-pipeline` | Produces `ContextReport` JSON for environment detection |
| `job-system-burst` | `06-performance` | `IJobParallelFor` + `[BurstCompile]`, 0 GC, 20× speedup templates |
| `service-locator-pattern` | `01-architecture` | Type-safe SL + DI decision matrix + bootstrapper |
| `mvvm-binding-system` | `05-ui-ux` | Full MVVM for UI Toolkit, `INotifyBindablePropertyChanged`, `[CreateProperty]` |

---

### ✨ Added — Batch B: Architecture & Backend Skills (8 skills)

| Skill | Category | Key Feature |
|-------|---------|------------|
| `coreclr-gc-watchdog` | `00-core-engineering` | GC pressure table + `Span<T>`, `ArrayPool<T>`, delegate caching |
| `csharp12-features-guide` | `00-core-engineering` | Feature safety matrix — which C#12 features are safe in `Update()` |
| `repository-pattern` | `01-architecture` | `IRepository<T>` + `InMemoryRepository` for TDD + async JSON impl |
| `command-pattern-undo` | `01-architecture` | Undo/Redo `CommandHistory` stack |
| `playfab-economy-v2` | `08-backend-monetization` | Economy v2 full guide (v1 deprecated) + `IPlayFabEconomyService` |
| `unity-gaming-services` | `08-backend-monetization` | UGS Auth, Lobby (heartbeat), Cloud Save, Leaderboards |
| `ads-mediation-ironsource` | `08-backend-monetization` | LevelPlay rewarded/interstitial/banner + GDPR consent flow |
| `metadata-validator` | `07-tools-pipeline` | PowerShell + Python compliance audit scripts |

---

### ✨ Added — Batch C: Visuals, Gameplay & Tools Skills (7 skills)

| Skill | Category | Key Feature |
|-------|---------|------------|
| `gpu-instancing-expert` | `06-performance` | `DrawMeshInstancedIndirect` with `ComputeBuffer` — 100k meshes/1 draw call |
| `texture-streaming-expert` | `06-performance` | Mip Streaming budget by platform + `TextureAuditTool` editor tool |
| `accessibility-hci` | `05-ui-ux` | WCAG 2.1, colorblind shader (3 modes), `InputActionRebindingExtensions` |
| `ai-code-reviewer` | `07-tools-pipeline` | CRITICAL/WARNING/INFO checklist with regex detection + scored report |
| `procedural-generation` | `02-gameplay` | BSP Dungeon + Perlin Noise Terrain sharing `IGrid<T>` API |
| `replay-system` | `02-gameplay` | Deterministic input recording, `InputTimeline` struct, death-cam integration |
| `minimap-system` | `02-gameplay` | Orthographic Camera → RenderTexture → UI panel + fog-of-war outline |

---

### 🔄 Changed

- **README.md** and **README.es.md**: Updated to 2026 Edition
  - Badges: `Unity 2023+` → `Unity 6+`, `C# 12`, `Skills 61` → `Skills 84`
  - Added 2026 Standard comparison table
  - Added Tier Architecture overview
  - Added Context Discovery Protocol section
  - Full catalog updated with all 84 skills and ⭐ new markers
- **Category `03-survival-city-builder`** renamed to **`03-simulation-strategy`** (agnosticism principle)

---

### 🛠️ Infrastructure

- **CHANGELOG.md**: Created (this file)
- **`SKILL_MASTER_TEMPLATE.md`**: Created as canonical 2026 reference

---

## [1.0.0] — 2025-01-01 — *"Initial Release"*

- 61 skills across 10 categories
- Unity 2023+ / Mono / C#10 target
- Convergence Standard v1 (name, description, tags, templates)

---

*AntiGravity Skills — Where Code Meets Intelligence.*
