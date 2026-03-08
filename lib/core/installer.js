// lib/core/installer.js
// Copies skill files into the target Unity project under:
//   Assets/Plugins/AntiGravitySkills/<skill-name>/
//
// Zero-lock-in: plain file copy, no compilation, no wrappers.
// Files are immediately editable by the developer.

import fs from 'node:fs';
import path from 'node:path';

import os from 'node:os';

const INSTALL_BASE = path.join('Assets', 'Plugins', 'AntiGravitySkills');

/**
 * Install a skill's files into the Unity project or globally.
 *
 * Priority:
 *   1. templates/ directory  → copy all .cs / .shader / .json files
 *   2. SKILL.md alone        → copy as reference documentation
 *
 * @param {object} opts
 * @param {string}   opts.projectRoot     - Unity project root (from ContextReport, nullable if global)
 * @param {string}   opts.skillName       - Name of the skill (folder name)
 * @param {string}   opts.skillContent    - Raw SKILL.md content
 * @param {string[]} opts.templateFiles   - Absolute paths to template files (may be empty)
 * @param {boolean}  opts.global          - Install to ~/.antigravity/skills instead of project
 * @returns {{ installedPath: string, files: string[] }}
 */
export function installSkill({ projectRoot, skillName, skillContent, templateFiles, global }) {
    let destDir;
    if (global) {
        destDir = path.join(os.homedir(), '.antigravity', 'skills', skillName);
    } else {
        destDir = path.join(projectRoot, INSTALL_BASE, skillName);
    }
    fs.mkdirSync(destDir, { recursive: true });

    const installed = [];

    if (templateFiles.length > 0) {
        // Copy template files (C#, shaders, configs)
        for (const src of templateFiles) {
            const dest = path.join(destDir, path.basename(src));
            fs.copyFileSync(src, dest);
            installed.push(dest);
        }
    }

    // Always install SKILL.md as in-project reference documentation
    const skillMdDest = path.join(destDir, 'SKILL.md');
    fs.writeFileSync(skillMdDest, skillContent, 'utf8');
    installed.push(skillMdDest);

    // Write a .gitkeep to ensure empty dirs aren't stripped
    if (installed.length === 1) {
        // Only SKILL.md — no templates, note this clearly
        const noteDest = path.join(destDir, 'README.md');
        fs.writeFileSync(noteDest,
            `# ${skillName}\n\nThis skill has no template files — consult SKILL.md for implementation guidance.\n`,
            'utf8'
        );
        installed.push(noteDest);
    }

    return { installedPath: destDir, files: installed };
}

/**
 * Check if a skill is already installed.
 * @param {string} projectRoot
 * @param {string} skillName
 * @param {boolean} global
 * @returns {boolean}
 */
export function isAlreadyInstalled(projectRoot, skillName, global = false) {
    if (global) {
        return fs.existsSync(path.join(os.homedir(), '.antigravity', 'skills', skillName));
    }
    return fs.existsSync(path.join(projectRoot, INSTALL_BASE, skillName));
}
