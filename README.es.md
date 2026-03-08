# 🌌 AntiGravity Skills
> *El "Córtex" para Desarrollo en Unity Nativo de IA — Edición 2026.*

[![Read in English](https://img.shields.io/badge/Read%20in-English-blue)](README.md)
![Unity](https://img.shields.io/badge/Unity-6%2B-black?logo=unity)
![CSharp](https://img.shields.io/badge/C%23-12-purple?logo=csharp)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Estado-Listo%20para%20Producción-blue)
![Skills](https://img.shields.io/badge/Skills-84_Activos-purple)
![Standard](https://img.shields.io/badge/Estándar-Edición%202026-gold)
![PeerReview](https://img.shields.io/badge/Peer%20Review-Validado-brightgreen)

---

## 👋 Bienvenidos al Futuro del Desarrollo de Videojuegos
**AntiGravity Skills** no es solo una librería de código — es un **Grafo de Conocimiento Estandarizado** diseñado para cerrar la brecha entre la creatividad Humana y la ejecución de la IA. Cada skill es portable, autocontenido y agnóstico al género, plataforma y proyecto.

*   **Para Agentes de IA (Gemini, Copilot, Cursor)**: Memoria a largo plazo + Líder Técnico Senior. Provee contexto, patrones de arquitectura y restricciones "no alucines" mediante la **Arquitectura de Niveles 2026**.
*   **Para Desarrolladores Humanos**: Un framework modular probado en batalla. ¿Necesitas un sistema? No lo escribas desde cero — invócalo.

> [!IMPORTANT]
> **🤖 Habilita la Persona de "Líder Técnico"**
> Cargar `AGENT.md` activa la persona de **Arquitecto AntiGravity**. El agente actúa como un **Mentor Senior** — explicando patrones SOLID, advirtiendo sobre presión GC, y aplicando el **protocolo TDD-First 2026** mientras construye.

---

## 🧩 ¿Qué es un Skill?
Un **Skill** es una unidad empaquetada de capacidad que conecta el razonamiento general con la ejecución específica de dominio. Cuando un Agente IA lee un `SKILL.md`, obtiene:

1.  **Conocimiento Procedimental**: Flujos de trabajo paso a paso para problemas específicos.
2.  **Conciencia Contextual**: Reglas y restricciones para prevenir errores comunes de Unity.
3.  **Plantillas**: Código C# pre-verificado listo para producción.

---

## 🆕 Estándar 2026 — ¿Qué Cambió?

| Característica | Antes | Edición 2026 |
|---------|--------|-------------|
| **Target Unity** | 2023+ | **Unity 6+ / CoreCLR** |
| **Lenguaje** | C#10 | **C#12 con Span\<T\>** |
| **Pre-vuelo** | Manual | **Protocolo de Context Discovery** |
| **Testing** | Opcional | **TDD-First (Obligatorio)** |
| **Política GC** | Guías | **Zero GC en hot paths** |
| **Metadatos del Skill** | Nombre + tags | **YAML completo: requirements, tiers, budgets** |

> [!NOTE]
> Los **84 skills** ahora llevan metadatos YAML completos del estándar 2026 (`requirements`, `context_discovery`, `performance_budget`, `tdd_first`). Los 20 skills nuevos son TDD-First nativos. Los 64 skills legacy llevan `tdd_first: false` y están marcados como *"Legacy — Refactorización Pendiente"* — es una señal honesta, no un defecto. Ver [Roadmap](#-roadmap--próximos-skills-v21) para el plan de mejora.

---

## 🏗️ Arquitectura del Sistema

```text
.agent/skills/
├── 00-core-engineering/      # C#12, GC Watchdog, Guías de Estilo
├── 01-architecture/          # Service Locator, Repository, Command, FSM, Eventos
├── 02-gameplay/              # Combate, Cámara, Minimapa, Replay, Generación Procedural
├── 03-simulation-strategy/   # Grid Building, Recursos, Oleadas  [Agnóstico 2026]
├── 04-visuals-audio/         # Shaders, VFX, Iluminación, Audio
├── 05-ui-ux/                 # MVVM, UI Toolkit, Accesibilidad (WCAG 2.1)
├── 06-performance/           # Job System, GPU Instancing, Texture Streaming
├── 07-tools-pipeline/        # Context Discovery, AI Code Reviewer, Validador
├── 08-backend-monetization/  # PlayFab Economy v2, UGS, Mediación de Ads
├── 09-devops-automation/     # CI/CD, Pipelines de Build
└── 00-meta-skills/           # Creador de Skills, Scaffolder de Proyectos
```

### Arquitectura de Niveles 2026

Cada skill opera en 3 niveles optimizados para IA:

| Nivel | Contenido | Consumido por |
|-------|---------|------------|
| **Nivel 1** | Frontmatter YAML (requirements, context_discovery, performance_budget) | Máquina — **gate de bloqueo duro** |
| **Nivel 2** | Cuerpo del SKILL.md (Cuándo usar, Arquitectura, Ejemplos de código) | Razonamiento IA |
| **Nivel 3** | Directorio `templates/` (archivos C#) | Inyección directa de código |

> [!IMPORTANT]
> **El Nivel 1 es un gate de bloqueo duro.** Si `requirements.unity_version` o `render_pipeline` no coinciden con el `ContextReport` del proyecto, el agente debe detenerse y reportar la incompatibilidad antes de escribir cualquier código. Continuar sin cumplir los requisitos requiere un override explícito `--force` del usuario, que el agente debe registrar visiblemente.

---

## 🏛️ Catálogo de Skills (84 Skills Activos)

### ⚙️ Ingeniería Core (`00-core-engineering`)
*   **`unified-style-guide`** — C#12, CoreCLR, reglas Zero GC
*   **`unity-compile-fixer`** ⭐ NUEVO — Bucle agnóstico de reparación de errores C#
*   **`coreclr-gc-watchdog`** ⭐ NUEVO — Clasificación de presión GC + patrones zero-alloc
*   **`csharp12-features-guide`** ⭐ NUEVO — Matriz de seguridad para features de C#12 en Unity 6

### 🏛 Arquitectura (`01-architecture`)
*   **`service-locator-pattern`** ⭐ NUEVO — SL type-safe con matriz de decisión DI
*   **`repository-pattern`** ⭐ NUEVO — `IRepository<T>` genérico con I/O async + mock
*   **`command-pattern-undo`** ⭐ NUEVO — Stack de historial Deshacer/Rehacer
*   **`event-bus-system`**, **`finite-state-machine`**, **`save-load-serialization`**, **`asynchronous-programming`**

### 🎮 Gameplay (`02-gameplay`)
*   **`procedural-generation`** ⭐ NUEVO — Mazmorra BSP + Terreno Perlin con `IGrid<T>`
*   **`replay-system`** ⭐ NUEVO — Grabación determinista de inputs + death-cam
*   **`minimap-system`** ⭐ NUEVO — Minimapa RenderTexture ortográfico con capas de iconos
*   **`player-movement-controller`**, **`camera-system-pro`**, **`combat-hitbox-system`**

### 🎯 Simulación y Estrategia (`03-simulation-strategy`)
*   **`grid-based-building-system`**, **`resource-management-system`**, **`horde-wave-logic`**, **`environment-hazard-system`**

### 🎨 Visuales y Audio (`04-visuals-audio`)
*   **`shader-graph-expert`**, **`vfx-graph-shuriken`**, **`dynamic-audio-mixers`**, **`lighting-nav-baker`**

### 🖥️ UI/UX (`05-ui-ux`)
*   **`mvvm-binding-system`** ⭐ NUEVO — MVVM completo para UI Toolkit con `[CreateProperty]`
*   **`accessibility-hci`** ⭐ NUEVO — WCAG 2.1, shaders de daltonismo, remapeo de controles
*   **`canvas-performance`**, **`responsive-ui-design`**, **`input-system-new`**

### ⚡ Rendimiento (`06-performance`)
*   **`job-system-burst`** ⭐ NUEVO — Unity Jobs + Burst Compiler (0 GC, CPU paralelo)
*   **`gpu-instancing-expert`** ⭐ NUEVO — `DrawMeshInstancedIndirect`, 100k meshes/draw call
*   **`texture-streaming-expert`** ⭐ NUEVO — Presupuesto Mip Streaming + `TextureAuditTool`
*   **`object-pooling-system`**, **`addressables-asset-management`**, **`memory-profiler-expert`**

### 🛠️ Herramientas y Pipeline (`07-tools-pipeline`)
*   **`context-discovery-agent`** ⭐ NUEVO — Detecta versión Unity, RP, paquetes → ContextReport
*   **`ai-code-reviewer`** ⭐ NUEVO — Checklist de revisión de código CRÍTICO/ADVERTENCIA/INFO
*   **`metadata-validator`** ⭐ NUEVO — Script de auditoría de compliance para todos los SKILL.md
*   **`automated-unit-testing`**, **`custom-editor-scripting`**, **`version-control-git`**

### 💰 Backend y Monetización (`08-backend-monetization`)
*   **`playfab-economy-v2`** ⭐ NUEVO — API Economy v2 (depreca v1), `IPlayFabEconomyService`
*   **`unity-gaming-services`** ⭐ NUEVO — UGS: Auth, Lobby, Relay, Leaderboards, Cloud Save
*   **`ads-mediation-ironsource`** ⭐ NUEVO — Rewarded/Interstitial LevelPlay + GDPR
*   **`analytics-heatmaps`**, **`monetization-iap`**, **`multiplayer-netcode`**

### 🚀 DevOps y Automatización (`09-devops-automation`)
*   **`build-pipeline-manager`**, **`unity-build-commander`**

---

## 🏷️ Etiquetas de Calidad de Skills

Cada skill lleva un campo `tdd_first:` que señala su nivel de calidad:

| Etiqueta | Significado | Qué esperar |
|----------|-------------|-------------|
| `tdd_first: true` ⭐ | Nativo 2026 | Interfaz + test fallido + implementación + mock. Listo para producción. |
| `tdd_first: false` 🔧 | Legacy — Refactorización Pendiente | Arquitectura sólida, pero sin scaffold TDD. Usar con revisión extra. |

> La honestidad importa: el agente usa `tdd_first` para calibrar la rigurosidad de su revisión. Un `false` señala que el agente debe ser más crítico con el código generado, no más tolerante.

---

## ⚡ Protocolo de Context Discovery 2026

Antes de generar cualquier código, el agente ejecuta un **chequeo pre-vuelo**:

```json
// Producido por @context-discovery-agent
{
  "unity_version": "6000.1.2f1",
  "render_pipeline": "URP",
  "awaitable_api": true,
  "burst_available": true,
  "packages": ["com.unity.inputsystem", "com.unity.services.core"]
}
```

Esto garantiza que cada script generado sea **compatible con tu entorno exacto** — sin más sorpresas de "esto solo funciona en HDRP".

---

## 🛠️ Flujo de Trabajo

### PARA AGENTES (El Bucle)
1.  **Detectar**: Ejecutar `@context-discovery-agent` → obtener `ContextReport`.
2.  **Encontrar**: Localizar el skill relevante en `.agent/skills/`.
3.  **Verificar**: Revisar `requirements:` en el frontmatter YAML contra el `ContextReport`.
4.  **Leer**: Consumir el cuerpo del SKILL.md para arquitectura + patrones.
5.  **Implementar**: Inyectar desde `templates/`, adaptar al contexto del proyecto.
6.  **Revisar**: Ejecutar `@ai-code-reviewer` antes de hacer commit.

### 🧑‍💻 PARA HUMANOS: Deja de generar código basura ("Vibe Coding")

El mayor error que cometen los desarrolladores con herramientas de IA (Copilot, Cursor, Gemini) es el **"Vibe Coding"** — pedirle a la IA que construya sistemas sin proporcionarle límites arquitectónicos estrictos. Esto resulta en código espagueti, fugas de memoria y juegos que no escalan.

La **CLI de AntiGravity Skills** resuelve esto inyectando patrones de nivel Senior, listos para producción, directamente en tu proyecto.

#### ¿Por qué usar esto?
*   **Para Juniors:** Deja de adivinar cómo construir un Object Pool o un Event Bus. La CLI inyecta código C# limpio, fuertemente comentado y con estándares de la industria directamente en tu proyecto para que lo estudies y uses.
*   **Para Seniors e IA:** Cada skill instalado incluye un archivo `SKILL.md` como "córtex". Cuando le pides a tu asistente de IA que modifique el código inyectado, la IA lee este archivo primero. Las reglas estrictas en su interior evitan que alucine o rompa la arquitectura.

#### Cómo usarlo (Cero Instalación)
Gracias a `npx`, **no necesitas instalar nada localmente ni clonar el repositorio**. La CLI verifica tu versión de Unity y Render Pipeline para prevenir errores, y luego inyecta código C# limpio ("Zero-Lock-In") en `Assets/Plugins/AntiGravitySkills/`.

Ejecútalo desde la raíz de tu proyecto en Unity:

```bash
# 1. Busca en el catálogo el sistema que necesitas
npx github:nlelouche/Unity3D-AntiGravitySkills list

# 2. Revisa sus requisitos (versión Unity, paquetes) antes de instalar
npx github:nlelouche/Unity3D-AntiGravitySkills info event-bus-system

# 3. Inyecta el código de forma segura en tu proyecto
npx github:nlelouche/Unity3D-AntiGravitySkills add event-bus-system
```

*Nota para Agentes de IA locales: Aún puedes clonar el repositorio completo en `.agent/skills/` si prefieres que tu agente tenga acceso permanente offline a todo el grafo de conocimiento.*
```bash
git clone https://github.com/nlelouche/Unity3D-AntiGravitySkills.git .agent/skills
```

---

## 🗺️ Roadmap — Próximos Skills v2.1

Basado en revisión arquitectónica y análisis de brechas, los siguientes skills son prioridad para la próxima iteración:

| Prioridad | Skill | Categoría | Justificación |
|-----------|-------|-----------|---------------|
| 🔴 Alta | `netcode-for-gameobjects` | `01-architecture` | Mayor brecha — único sistema core de Unity 6 sin cobertura |
| 🔴 Alta | `localization-unity-package` | `07-tools-pipeline` | El setup de `StringTable` + `LocalizeStringEvent` es un pain-point clave para IA |
| 🟡 Media | `xr-toolkit-vr` | `02-gameplay` | Crecimiento del mercado VR/MR (Quest 3, Vision Pro) — skill XR agnóstico de plataforma |
| 🟡 Media | `dots-physics` | `06-performance` | Complemento natural de `job-system-burst` para simulaciones con física intensiva |
| 🟢 Baja | `websockets-native` | `08-backend-monetization` | Parcialmente cubierto por UGS Relay — menor prioridad salvo proyectos sin UGS |

---

## 📊 Estadísticas del Repositorio (Edición 2026)

| Categoría | Skills | TDD-Nativo |
|:---------|:------:|:----------:|
| Ingeniería Core | 4 | 3 |
| Meta Skills | 3 | 0 |
| Arquitectura | 13 | 3 |
| Gameplay | 14 | 3 |
| Simulación y Estrategia | 6 | 0 |
| Visuales y Audio | 9 | 0 |
| UI/UX | 8 | 2 |
| Rendimiento | 8 | 3 |
| Herramientas y Pipeline | 9 | 4 |
| Backend y Monetización | 8 | 3 |
| DevOps y Automatización | 2 | 0 |
| **GRAN TOTAL** | **84** | **20** |

---

## 🗂️ CHANGELOG

Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo.

---

**AntiGravity Skills** — *Donde el Código Encuentra la Inteligencia. Edición 2026.*
