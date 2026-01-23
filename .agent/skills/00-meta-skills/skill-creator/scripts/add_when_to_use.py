#!/usr/bin/env python3
"""
When to Use Section Generator
Adds a "When to Use" section to all SKILL.md files based on their description and content.
"""

import os
import re
from pathlib import Path
import argparse

# Mapping of skill patterns to when-to-use bullets
SKILL_PATTERNS = {
    # Architecture skills
    "bootstrap": ["starting a new Unity project", "setting up initial architecture", "establishing project foundations"],
    "event": ["implementing decoupled communication", "creating publish-subscribe patterns", "reducing dependencies between systems"],
    "state-machine": ["managing state transitions", "creating game states", "implementing character states"],
    "scriptableobject": ["creating data-driven systems", "sharing data between objects", "implementing SO architecture"],
    "interface": ["defining contracts between systems", "implementing dependency injection", "creating testable code"],
    "async": ["handling asynchronous operations", "implementing async/await patterns", "managing coroutines vs Tasks"],
    "pattern": ["implementing design patterns", "solving common architecture problems", "improving code structure"],
    "dots": ["implementing ECS systems", "high-performance data-oriented code", "DOTS/Burst optimization"],
    "di-container": ["setting up dependency injection", "managing service lifetimes", "implementing IoC containers"],
    
    # Gameplay skills
    "behavior-tree": ["creating AI decision making", "implementing NPC behaviors", "patrol/attack/flee logic"],
    "character-controller": ["implementing player movement", "3D/2D character physics", "custom character controllers"],
    "save-load": ["implementing save systems", "persisting game data", "serialization/deserialization"],
    "inventory": ["creating inventory systems", "item management", "crafting mechanics"],
    "loot": ["implementing drop tables", "random rewards", "weighted RNG systems"],
    "damage": ["creating health systems", "damage calculation", "death/respawn logic"],
    "ability": ["implementing skill systems", "cooldown management", "ability effects"],
    "status-effect": ["buff/debuff systems", "temporary stat modifications", "poison/burn effects"],
    "dialogue": ["conversation systems", "quest dialogues", "NPC interactions"],
    "quest": ["quest tracking", "objective systems", "mission progression"],
    "navmesh": ["AI pathfinding", "navigation agent setup", "obstacle avoidance"],
    "physics": ["physics-based interactions", "rigidbody mechanics", "collision handling"],
    
    # Survival/City Builder
    "resource": ["resource gathering", "economy systems", "production chains"],
    "building": ["construction systems", "grid-based placement", "building mechanics"],
    "wave": ["wave-based spawning", "enemy waves", "horde survival mechanics"],
    "hazard": ["environmental dangers", "trap systems", "damage zones"],
    "tech-tree": ["research systems", "upgrade trees", "unlock progression"],
    "population": ["unit management", "AI crowds", "worker assignment"],
    
    # Visual/Audio
    "cinemachine": ["camera systems", "virtual cameras", "cutscenes"],
    "audio": ["audio management", "sound effects", "music systems"],
    "juice": ["game feel", "screen shake", "visual feedback"],
    "lighting": ["lighting setup", "post-processing", "visual atmosphere"],
    "animation": ["procedural animation", "IK systems", "animation blending"],
    "shader": ["custom shaders", "visual effects", "material programming"],
    "vfx": ["particle systems", "visual effects", "VFX Graph"],
    
    # UI/UX
    "canvas": ["UI performance", "canvas optimization", "rendering efficiency"],
    "input": ["input handling", "New Input System", "control schemes"],
    "menu": ["menu systems", "UI navigation", "settings screens"],
    "ui-toolkit": ["UI Toolkit development", "USS styling", "UXML layouts"],
    "responsive": ["adaptive UI", "multi-resolution support", "safe areas"],
    
    # Performance
    "addressables": ["asset management", "content loading", "memory optimization"],
    "pooling": ["object pooling", "spawn optimization", "memory efficiency"],
    "lod": ["level of detail", "occlusion culling", "rendering optimization"],
    "profiler": ["performance analysis", "memory debugging", "frame timing"],
    "mobile": ["mobile optimization", "platform constraints", "battery/thermal"],
    
    # Backend/Services
    "playfab": ["PlayFab integration", "backend services", "cloud data"],
    "analytics": ["event tracking", "player metrics", "heatmaps"],
    "multiplayer": ["Netcode", "networking", "multiplayer sync"],
    "iap": ["in-app purchases", "monetization", "store integration"],
    
    # Tools/Pipeline
    "build": ["automated builds", "CI/CD", "build pipeline"],
    "testing": ["unit testing", "test automation", "TDD"],
    "editor": ["custom inspectors", "editor windows", "tooling"],
    "localization": ["multi-language support", "translation", "localization"],
    "git": ["version control", "Git workflow", "branching strategy"],
    "mcp": ["Unity MCP", "AI integration", "automated scene editing"],
}


def get_when_to_use(skill_name: str, description: str) -> list[str]:
    """Generate When to Use bullets based on skill name and description."""
    bullets = []
    
    name_lower = skill_name.lower()
    desc_lower = description.lower()
    
    # Find matching patterns
    for pattern, use_cases in SKILL_PATTERNS.items():
        if pattern in name_lower or pattern in desc_lower:
            bullets.extend(use_cases)
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for b in bullets:
        if b not in seen:
            seen.add(b)
            unique.append(b)
    
    # If no matches, generate generic ones from description
    if not unique:
        # Extract quoted phrases from description as triggers
        quotes = re.findall(r'"([^"]+)"', description)
        for q in quotes[:3]:
            unique.append(q.lower().strip())
    
    # Limit to 5 bullets
    return unique[:5] if unique else ["implementing this feature", "following best practices", "automating this workflow"]


def add_when_to_use_section(content: str, skill_name: str, description: str) -> tuple[str, bool]:
    """Add When to Use section after Overview/Goal section if not present."""
    
    # Check if already has When to Use
    if re.search(r'^## When to Use', content, re.MULTILINE):
        return content, False
    
    # Get bullets
    bullets = get_when_to_use(skill_name, description)
    
    # Create section
    when_section = "\n## When to Use\n"
    for bullet in bullets:
        when_section += f"- Use when {bullet}\n"
    
    # Find insertion point: after Goal, Overview, or first H1
    patterns = [
        (r'(## Goal\s*\n(?:[^\n#]+\n)*)', r'\1' + when_section),  # After Goal section
        (r'(## Overview\s*\n(?:[^\n#]+\n)*)', r'\1' + when_section),  # After Overview
        (r'(# [^\n]+\n\n)', r'\1' + when_section),  # After H1 title
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content, count=1)
            if new_content != content:
                return new_content, True
    
    # Fallback: add after frontmatter
    parts = content.split('---', 2)
    if len(parts) >= 3:
        return f"{parts[0]}---{parts[1]}---{when_section}\n{parts[2]}", True
    
    return content, False


def process_skill(skill_path: Path, dry_run: bool = True) -> dict:
    """Process a single skill file."""
    report = {'path': str(skill_path), 'updated': False, 'error': None}
    
    try:
        content = skill_path.read_text(encoding='utf-8')
    except Exception as e:
        report['error'] = str(e)
        return report
    
    if not content.strip():
        report['error'] = 'Empty file'
        return report
    
    # Extract frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        report['error'] = 'No frontmatter'
        return report
    
    # Get name and description
    name_match = re.search(r'^name:\s*(.+)$', fm_match.group(1), re.MULTILINE)
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', fm_match.group(1), re.MULTILINE)
    
    skill_name = name_match.group(1).strip() if name_match else skill_path.parent.name
    description = desc_match.group(1).strip() if desc_match else ""
    
    # Add section
    new_content, updated = add_when_to_use_section(content, skill_name, description)
    
    if updated:
        report['updated'] = True
        if not dry_run:
            skill_path.write_text(new_content, encoding='utf-8')
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Add When to Use sections to skills')
    parser.add_argument('--skills-path', '-p', default='.agent/skills')
    parser.add_argument('--apply', '-a', action='store_true', help='Apply changes')
    args = parser.parse_args()
    
    base_path = Path(args.skills_path)
    if not base_path.exists():
        print(f"Path not found: {base_path}")
        return 1
    
    dry_run = not args.apply
    skills = list(base_path.rglob('SKILL.md'))
    
    print(f"Found {len(skills)} skill files")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLYING CHANGES'}\n")
    
    updated = 0
    errors = 0
    skipped = 0
    
    for skill in skills:
        report = process_skill(skill, dry_run)
        if report['error']:
            print(f"[ERROR] {skill.parent.name}: {report['error']}")
            errors += 1
        elif report['updated']:
            print(f"[UPDATE] {skill.parent.name}")
            updated += 1
        else:
            skipped += 1
    
    print(f"\n{'='*50}")
    print(f"Updated: {updated}")
    print(f"Skipped (already has section): {skipped}")
    print(f"Errors: {errors}")
    
    if dry_run:
        print("\nDRY RUN - no changes made. Use --apply to apply.")
    
    return 0


if __name__ == '__main__':
    exit(main())
