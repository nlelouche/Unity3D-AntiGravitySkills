# Definicion de la estructura de Skills para Unity
$skillsStructure = @{
    "01-architecture" = @(
        "scriptableobject-architecture", "advanced-design-patterns", "dependency-injection",
        "interface-driven-development", "state-machine-architect", "dots-ecs",
        "asynchronous-programming", "event-bus-system"
    )
    "02-gameplay" = @(
        "advanced-character-controller", "ability-skill-system", "inventory-crafting-logic",
        "damage-health-framework", "ai-behavior-trees", "navmesh-pathfinding",
        "loot-rng-management", "dialogue-quest-system", "save-load-serialization",
        "physics-logic"
    )
    "03-survival-city-builder" = @(
        "resource-management-system", "grid-based-building-system", "horde-wave-logic",
        "tech-tree-research", "unit-population-ai", "environment-hazard-system"
    )
    "04-visuals-audio" = @(
        "shader-graph-expert", "vfx-graph-shuriken", "procedural-animation-ik",
        "cinemachine-specialist", "lighting-post-processing", "dynamic-audio-mixers",
        "juice-game-feel"
    )
    "05-ui-ux" = @(
        "ui-toolkit-modern", "canvas-performance", "responsive-ui-design",
        "input-system-new", "menu-navigation-flow"
    )
    "06-performance" = @(
        "object-pooling-system", "addressables-asset-management", "memory-profiler-expert",
        "mobile-optimization", "lod-occlusion-culling"
    )
    "07-tools-pipeline" = @(
        "custom-editor-scripting", "automated-unit-testing", "ci-cd-unity",
        "localization-specialist", "version-control-git"
    )
    "08-backend-monetization" = @(
        "multiplayer-netcode", "backend-integration", "monetization-iap",
        "analytics-heatmaps"
    )
}

# Crear la carpeta base .agent/skills
$basePath = ".agent/skills"
if (!(Test-Path $basePath)) {
    New-Item -ItemType Directory -Path $basePath -Force | Out-Null
    Write-Host "Carpeta base creada: $basePath" -ForegroundColor Green
}

# Iterar sobre las categorias y crear carpetas y archivos
foreach ($category in $skillsStructure.Keys) {
    $categoryPath = Join-Path $basePath $category
    
    foreach ($skill in $skillsStructure[$category]) {
        $skillPath = Join-Path $categoryPath $skill
        
        # Crear la carpeta del skill si no existe
        if (!(Test-Path $skillPath)) {
            New-Item -ItemType Directory -Path $skillPath -Force | Out-Null
        }
        
        # Crear el archivo skill.md vacio
        $filePath = Join-Path $skillPath "skill.md"
        if (!(Test-Path $filePath)) {
            New-Item -ItemType File -Path $filePath -Force | Out-Null
            Write-Host "Creado: $category/$skill/skill.md" -ForegroundColor Cyan
        }
    }
}

Write-Host "Estructura de 50 Skills completada!" -ForegroundColor Magenta