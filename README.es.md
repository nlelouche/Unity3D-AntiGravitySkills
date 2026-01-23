# 🌌 AntiGravity Skills
> *El "Córtex" para Desarrollo en Unity Nativo de IA.*

[![Read in English](https://img.shields.io/badge/Read%20in-English-blue)](README.md)
![Unity](https://img.shields.io/badge/Unity-2023%2B-black?logo=unity)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Estado-Listo%20para%20Producci%C3%B3n-blue)
![Skills](https://img.shields.io/badge/Skills-61_Activos-purple)
![Templates](https://img.shields.io/badge/Plantillas-96_Listas-orange)

---

## 👋 Bienvenidos al Futuro del Desarrollo de Videojuegos
**AntiGravity Skills** no es solo una librería de código—es un **Grafo de Conocimiento Estandarizado** diseñado para cerrar la brecha entre la creatividad Humana y la ejecución de la IA.

*   **Para Agentes de IA (Gemini, Copilot, Cursor)**: Este repositorio actúa como tu **Memoria a Largo Plazo** y **Líder Técnico Senior**. Provee contexto, patrones de arquitectura y restricciones para "no alucinar".
*   **Para Desarrolladores Humanos**: Es un framework modular probado en batalla. ¿Necesitas un sistema? No lo escribas desde cero; invócalo.

---

## 🧩 ¿Qué es un "Skill"?
En el contexto de Agentes IA Autónomos, un **Skill** (Habilidad) es una unidad empaquetada de capacidad que une el razonamiento general con la ejecución específica de dominio.

Así como un ingeniero humano consultaría un manual técnico o a un mentor, un Agente IA "se equipa" un Skill para ganar:
1.  **Conocimiento Procedimental**: Flujos de trabajo paso a paso sobre *cómo* resolver un problema específico.
2.  **Conciencia Contextual**: Restricciones y reglas (ej: "Siempre usa `StringBuilder` aquí") para prevenir errores comunes.
3.  **Herramientas y Plantillas**: Assets de código pre-verificados que aseguran que el resultado está listo para producción.

Para una inmersión profunda en la arquitectura y protocolo de Skills, consulta la **[Documentación Oficial de AntiGravity](https://antigravity.google/docs/skills)**.

---

## 🚀 ¿Por qué AntiGravity?

### 🧠 Características para Agentes IA
*   **Inyección de Contexto**: Deja de adivinar. Lee los archivos `SKILL.md` para entender la arquitectura *exacta* requerida antes de escribir una sola línea de código.
*   **Precisión Zero-Shot**: Usa las `templates/` (plantillas) provistas para implementar sistemas complejos (FSMs, Inventario, Netcode) correctamente al primer intento.
*   **Estandarización**: Cada script sigue namespaces, formato y patrones específicos (SOLID, inyección de dependencias), asegurando que el código nuevo encaje perfectamente.

### 👤 Beneficios para Humanos
*   **Arquitectura Plug-and-Play**: ¿Necesitas una "Cámara en Tercera Persona"? Invoca `@cinemachine-specialist`. ¿Necesitas "Inventario"? Invoca `@inventory-crafting-logic`.
*   **Estándares de Producción**: Desde "Greybox" hasta "Gold Master", los skills cubren cada fase de producción incluyendo DevOps, Analíticas y Optimización.
*   **Deuda Técnica Reducida**: El código generado vía estos skills está pre-arquitectado para ser desacoplado y testeable.

---

## 🏗️ Arquitectura del Sistema

El repositorio está estructurado para ingestión automática por agentes habilitados con MCP.

```text
.agent/skills/
├── 00-core-engineering/      # Estándares de Código y Guías de Estilo
├── 01-architecture/          # Sistemas Core (Eventos, FSM, Guardado)
├── 02-gameplay/              # Mecánicas (Combate, Cámara, Input)
├── 03-survival-city-builder/ # Género: Supervivencia y Estrategia
├── 04-visuals-audio/         # Shaders, VFX, SFX
├── 04-devops-automation/     # CI/CD, Pipelines de Build
├── 05-ui-ux/                 # MVVM UI, Toolkits, HUDs
├── 06-performance/           # Optimización, Memoria, Object Pooling
├── 07-tools-pipeline/        # Herramientas de Editor, Importación, Git
├── 08-backend-monetization/  # Analíticas, IAP, Multiplayer
└── 00-meta-skills/           # Auto-replicación de Agente y Liderazgo
```

### Anatomía de un Skill
Cada skill sigue el **"Estándar de Convergencia"**:
1.  **`SKILL.md`**: El cerebro. Contiene el "Cuándo usar", "Diagramas de Arquitectura", y "Ejemplos de Prompting Few-Shot".
2.  **`templates/`**: Scripts C#, Shaders, o Configs que están al 90% completos y listos para desplegar.
3.  **`examples/`**: (Opcional) Escenas de referencia o ejemplos de uso.

---

## 🏛️ Catálogo de Skills (Los 12 Pilares)

### 1. Ingeniería Core (`00-core`)
*   **`unified-style-guide`**: La ley suprema para el formato de C#.

### 2. Arquitectura (`01-architecture`)
*   **`service-locator-pattern`**: Gestión de sistemas desacoplados.
*   **`event-bus-system`**: Mensajería global sin dependencias.
*   **`finite-state-machine`**: IA robusta y estados del jugador.
*   **`save-load-serialization`**: Persistencia y encriptación JSON/Binaria.
*   **`asynchronous-programming`**: Gestión de UniTask y Corutinas.

### 3. Gameplay (`02-gameplay`)
*   **`player-movement-controller`**: Controladores cinemáticos y basados en físicas.
*   **`camera-system-pro`**: Orquestación de Cinemachine.
*   **`universal-input-handler`**: Wrapper del New Input System.
*   **`combat-hitbox-system`**: Detección de daño confiable.

### 4. Supervivencia y Estrategia (`03-survival-city-builder`)
*   **`grid-based-building-system`**: Lógica de colocación para city builders.
*   **`resource-management-system`**: Inventario y economía.
*   **`horde-wave-logic`**: Spawners para tower defense/survival.
*   **`environment-hazard-system`**: Temperatura, hambre y sed.

### 5. Visuales y Audio (`04-visuals-audio`)
*   **`shader-graph-master`**: Plantillas de materiales.
*   **`particle-system-pro`**: Implementación de VFX.
*   **`audio-soundscape-architect`**: Gestión de mixers y audio espacial.
*   **`lighting-nav-baker`**: Automatización para Lightmapping y NavMesh.

### 6. DevOps y Automatización (`04-devops`)
*   **`build-pipeline-manager`**: Builds "Headless" por CLI para CI/CD.

### 7. UI/UX (`05-ui-ux`)
*   **`ui-toolkit-modern`**: Flujos de trabajo USS/UXML.
*   **`mvvm-pattern`**: Binding Modelo-Vista-ViewModel.
*   **`responsive-ui`**: Soporte multi-resolución.

### 8. Rendimiento (`06-performance`)
*   **`object-pooling-system`**: Spawneado sin alojar memoria (Zero-alloc).
*   **`addressables-asset-management`**: Carga asíncrona y cuidado de memoria.
*   **`memory-profiler-expert`**: Detección de fugas (leaks).

### 9. Herramientas y Pipeline (`07-tools-pipeline`)
*   **`asset-import-pipeline`**: Auto-compresión de texturas/modelos al importar.
*   **`custom-editor-scripting`**: Herramientas de inspector y ventanas.
*   **`automated-unit-testing`**: Plantillas NUnit (EditMode y PlayMode).
*   **`version-control-git`**: Automatización de `.gitignore` y LFS.

### 10. Backend y Monetización (`08-backend`)
*   **`analytics-heatmaps`**: Rastreo de telemetría.
*   **`monetization-iap`**: Wrapper de Unity Purchasing.
*   **`backend-integration`**: Guardado en nube y login (PlayFab/Firebase).
*   **`multiplayer-netcode`**: Setup de NGO (Netcode for GameObjects).

### 11. Meta Skills (`00-meta`)
*   **`skill-creator`**: Herramientas para crear nuevos skills.
*   **`project-scaffolder`**: Generación inicial de carpetas.
*   **`virtual-production-lead`**: Director IA que lee GDDs y planea hojas de ruta.

---

## 🛠️ Flujo de Trabajo: Cómo usar

### PARA AGENTES (El Bucle)
1.  **Analizar**: El usuario pide una funcionalidad (ej: "Haz un spawner de oleadas").
2.  **Buscar**: Mirar en `.agent/skills/`. Encontrar `@horde-wave-logic`.
3.  **Leer**: Consumir `SKILL.md` para aprender la arquitectura.
4.  **Implementar**: Usar `templates/WaveSpawner.cs.txt` como base.
5.  **Refinar**: Adaptar la plantilla a los requerimientos específicos del usuario.

### PARA HUMANOS (Instalación)
Clona este repositorio en la raíz de tu proyecto o como un submódulo:

```bash
git clone https://github.com/YourOrg/AntiGravitySkills.git .agent/skills
```

O ejecuta el script de configuración para iniciar un nuevo espacio de trabajo:

```powershell
# Windows
.\Initialize.ps1
```

```bash
# Mac/Linux
./setup.sh
```

---

## 📊 Estadísticas del Repositorio

| Categoría | Skills Autenticados | Plantillas Listas |
|:---------|:--------------------:|:---------------:|
| Arquitectura | 10 | 29 |
| Gameplay | 11 | 26 |
| Visuals & Audio | 8 | 10 |
| UI/UX | 5 | 5 |
| Survival/Strategy | 6 | 6 |
| Performance | 5 | 3 |
| Herramientas | 5 | 4 |
| Backend Ops | 4 | 4 |
| DevOps & Pipeline | 4 | 4 |
| Core/Meta/Lead | 3 | 5 |
| **GRAN TOTAL** | **61** | **96** |

---

**AntiGravity Skills** — *Donde el Código Encuentra la Inteligencia.*
