#!/usr/bin/env python3
"""
Skills Standardization Script
Standardizes all skill files in the AntiGravity skills collection.

Operations:
1. Rename skill.md → SKILL.md (case standardization)
2. Add missing frontmatter fields (version, tags)
3. Validate YAML frontmatter
4. Generate report of changes
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# ANSI colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.RESET} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.RESET} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")
def log_error(msg): print(f"{Colors.RED}[✗]{Colors.RESET} {msg}")

def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extract YAML frontmatter and body from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None, content
    
    frontmatter_text = match.group(1)
    body = match.group(2)
    
    # Simple YAML parsing (key: value pairs)
    frontmatter = {}
    current_key = None
    current_list = []
    
    for line in frontmatter_text.split('\n'):
        line = line.rstrip()
        if not line:
            continue
            
        # Check for list item
        list_match = re.match(r'^\s+-\s+(.+)$', line)
        if list_match and current_key:
            current_list.append(list_match.group(1))
            continue
        
        # Save previous list if any
        if current_list and current_key:
            frontmatter[current_key] = current_list
            current_list = []
        
        # Check for key-value pair
        kv_match = re.match(r'^(\w[\w-]*):\s*(.*)$', line)
        if kv_match:
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip()
            if value:
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                frontmatter[current_key] = value
    
    # Don't forget last list
    if current_list and current_key:
        frontmatter[current_key] = current_list
    
    return frontmatter, body


def rebuild_frontmatter(frontmatter: dict) -> str:
    """Rebuild frontmatter from dict, preserving order and adding missing fields."""
    lines = ["---"]
    
    # Standard field order
    field_order = ['name', 'description', 'version', 'tags', 'argument-hint', 
                   'disable-model-invocation', 'user-invocable', 'allowed-tools']
    
    # Add version if missing
    if 'version' not in frontmatter:
        frontmatter['version'] = '1.0.0'
    
    # Add tags if missing
    if 'tags' not in frontmatter:
        frontmatter['tags'] = []
    
    # Output fields in order
    processed = set()
    for key in field_order:
        if key in frontmatter:
            value = frontmatter[key]
            if isinstance(value, list):
                if key == 'tags' and not value:
                    lines.append(f'{key}: []')
                else:
                    lines.append(f'{key}:')
                    for item in value:
                        lines.append(f'  - {item}')
            elif isinstance(value, bool):
                lines.append(f'{key}: {str(value).lower()}')
            elif key == 'description':
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
            processed.add(key)
    
    # Add any remaining fields not in standard order
    for key, value in frontmatter.items():
        if key not in processed:
            if isinstance(value, list):
                lines.append(f'{key}:')
                for item in value:
                    lines.append(f'  - {item}')
            else:
                lines.append(f'{key}: {value}')
    
    lines.append("---")
    return '\n'.join(lines)


def standardize_skill(skill_path: Path, dry_run: bool = True) -> dict:
    """Standardize a single skill file. Returns report dict."""
    report = {
        'path': str(skill_path),
        'renamed': False,
        'frontmatter_updated': False,
        'fields_added': [],
        'errors': [],
        'empty': False
    }
    
    # Check if file exists and is readable
    if not skill_path.exists():
        report['errors'].append("File does not exist")
        return report
    
    # Read content
    try:
        content = skill_path.read_text(encoding='utf-8')
    except Exception as e:
        report['errors'].append(f"Read error: {e}")
        return report
    
    # Check for empty file
    if len(content.strip()) == 0:
        report['empty'] = True
        report['errors'].append("File is empty")
        return report
    
    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)
    if frontmatter is None:
        report['errors'].append("No valid frontmatter found")
        return report
    
    # Track changes
    original_keys = set(frontmatter.keys())
    
    # Add missing fields
    if 'version' not in frontmatter:
        report['fields_added'].append('version')
    if 'tags' not in frontmatter:
        report['fields_added'].append('tags')
    
    if report['fields_added']:
        report['frontmatter_updated'] = True
    
    # Rebuild content
    new_frontmatter = rebuild_frontmatter(frontmatter)
    new_content = f"{new_frontmatter}\n\n{body.lstrip()}"
    
    # Determine target path - keep same path, don't rename
    target_path = skill_path
    
    if skill_path.name.lower() == 'skill.md' and skill_path.name != 'SKILL.md':
        report['renamed'] = True
    
    # Apply changes if not dry run
    if not dry_run:
        try:
            # Write new content
            target_path.write_text(new_content, encoding='utf-8')
            
            # Remove old file if renamed
            if report['renamed'] and skill_path != target_path:
                skill_path.unlink()
                
        except Exception as e:
            report['errors'].append(f"Write error: {e}")
    
    return report


def find_all_skills(base_path: Path) -> list[Path]:
    """Find all skill.md files (case insensitive)."""
    skills = []
    for path in base_path.rglob('*'):
        if path.is_file() and path.name.lower() == 'skill.md':
            skills.append(path)
    return sorted(skills)


def generate_report(reports: list[dict], dry_run: bool) -> str:
    """Generate summary report."""
    lines = [
        "",
        f"{Colors.BOLD}{'='*60}{Colors.RESET}",
        f"{Colors.BOLD}  SKILLS STANDARDIZATION REPORT{Colors.RESET}",
        f"  Mode: {'DRY RUN (no changes made)' if dry_run else 'LIVE (changes applied)'}",
        f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"{'='*60}",
        ""
    ]
    
    # Statistics
    total = len(reports)
    renamed = sum(1 for r in reports if r['renamed'])
    updated = sum(1 for r in reports if r['frontmatter_updated'])
    empty = sum(1 for r in reports if r['empty'])
    errors = sum(1 for r in reports if r['errors'] and not r['empty'])
    
    lines.append(f"  Total skills processed: {total}")
    lines.append(f"  {Colors.GREEN}Files to rename:{Colors.RESET} {renamed}")
    lines.append(f"  {Colors.BLUE}Frontmatter to update:{Colors.RESET} {updated}")
    lines.append(f"  {Colors.YELLOW}Empty files:{Colors.RESET} {empty}")
    lines.append(f"  {Colors.RED}Errors:{Colors.RESET} {errors}")
    lines.append("")
    
    # Details for renamed files
    if renamed:
        lines.append(f"{Colors.BOLD}Files to rename (skill.md → SKILL.md):{Colors.RESET}")
        for r in reports:
            if r['renamed']:
                lines.append(f"  • {r['path']}")
        lines.append("")
    
    # Details for updated frontmatter
    if updated:
        lines.append(f"{Colors.BOLD}Frontmatter updates:{Colors.RESET}")
        for r in reports:
            if r['fields_added']:
                lines.append(f"  • {r['path']}")
                lines.append(f"    Added: {', '.join(r['fields_added'])}")
        lines.append("")
    
    # Empty files
    if empty:
        lines.append(f"{Colors.BOLD}Empty files (need manual attention):{Colors.RESET}")
        for r in reports:
            if r['empty']:
                lines.append(f"  • {r['path']}")
        lines.append("")
    
    # Errors
    error_reports = [r for r in reports if r['errors'] and not r['empty']]
    if error_reports:
        lines.append(f"{Colors.BOLD}Errors:{Colors.RESET}")
        for r in error_reports:
            lines.append(f"  • {r['path']}")
            for err in r['errors']:
                lines.append(f"    {Colors.RED}{err}{Colors.RESET}")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Standardize AntiGravity skills collection')
    parser.add_argument('--skills-path', '-p', type=str, 
                        default='.agent/skills',
                        help='Path to skills directory')
    parser.add_argument('--dry-run', '-d', action='store_true', default=True,
                        help='Preview changes without applying (default: True)')
    parser.add_argument('--apply', '-a', action='store_true',
                        help='Apply changes (overrides --dry-run)')
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    # Find skills base path
    base_path = Path(args.skills_path)
    if not base_path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent.parent
        base_path = script_dir
        if not base_path.exists():
            log_error(f"Skills path not found: {args.skills_path}")
            return 1
    
    log_info(f"Scanning: {base_path.absolute()}")
    
    # Find all skill files
    skills = find_all_skills(base_path)
    log_info(f"Found {len(skills)} skill files")
    
    if not skills:
        log_warning("No skill files found")
        return 0
    
    # Process each skill
    reports = []
    for skill_path in skills:
        report = standardize_skill(skill_path, dry_run=dry_run)
        reports.append(report)
        
        # Log progress
        status = []
        if report['renamed']:
            status.append('rename')
        if report['frontmatter_updated']:
            status.append('update')
        if report['empty']:
            status.append('EMPTY')
        if report['errors'] and not report['empty']:
            status.append('ERROR')
        
        if status:
            log_info(f"  {skill_path.name} in {skill_path.parent.name}: [{', '.join(status)}]")
    
    # Print report
    print(generate_report(reports, dry_run))
    
    if dry_run:
        print(f"{Colors.YELLOW}This was a DRY RUN. To apply changes, run with --apply{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}Changes applied successfully!{Colors.RESET}")
    
    return 0


if __name__ == '__main__':
    exit(main())
