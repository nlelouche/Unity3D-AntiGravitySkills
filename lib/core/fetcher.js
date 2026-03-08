// lib/core/fetcher.js
// Resolves where to read a skill's files from:
//   1. LOCAL  — if running inside the AntiGravitySkills repo (.agent/skills/ exists)
//   2. REMOTE — fetches SKILL.md from GitHub raw content as fallback

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '../../');
const SKILLS_DIR = path.join(REPO_ROOT, '.agent', 'skills');
const INDEX_PATH = path.join(REPO_ROOT, 'skills-index.json');

const GITHUB_RAW = 'https://raw.githubusercontent.com/nlelouche/Unity3D-AntiGravitySkills/main';

/** Load the bundled skills index */
function loadIndex() {
    if (!fs.existsSync(INDEX_PATH)) return {};
    const raw = fs.readFileSync(INDEX_PATH, 'utf8').replace(/^\uFEFF/, '');
    return JSON.parse(raw);
}

/**
 * Resolve the skill entry from the index.
 * @param {string} skillName
 * @returns {{ category: string, path: string, tdd_first: boolean, description: string }|null}
 */
export function resolveSkillMeta(skillName) {
    const index = loadIndex();
    // Support both exact match and fuzzy name (lowercase, no dashes)
    const direct = index[skillName];
    if (direct) return { name: skillName, ...direct };

    // Fuzzy fallback
    const key = Object.keys(index).find(
        k => k.toLowerCase().replace(/-/g, '') === skillName.toLowerCase().replace(/-/g, '')
    );
    return key ? { name: key, ...index[key] } : null;
}

/**
 * Read a skill's SKILL.md content — local first, GitHub remote fallback.
 * @param {{ path: string }} meta
 * @returns {Promise<string>} file content
 */
export async function fetchSkillContent(meta) {
    const localPath = path.join(REPO_ROOT, meta.path.replace(/\//g, path.sep));

    // Try local first
    if (fs.existsSync(localPath)) {
        return fs.readFileSync(localPath, 'utf8');
    }

    // Remote fallback via GitHub
    const url = `${GITHUB_RAW}/${meta.path}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch skill from GitHub: ${url} (${response.status})`);
    return response.text();
}

/**
 * List all files in a skill's templates/ directory (local only).
 * Returns [] if running remotely (templates must be fetched separately).
 * @param {{ path: string }} meta
 * @returns {string[]} absolute file paths
 */
export function listTemplateFiles(meta) {
    const skillDir = path.dirname(path.join(REPO_ROOT, meta.path.replace(/\//g, path.sep)));
    const templatesDir = path.join(skillDir, 'templates');
    if (!fs.existsSync(templatesDir)) return [];
    return fs.readdirSync(templatesDir).map(f => path.join(templatesDir, f));
}

/**
 * Return all skill names from the index.
 * @returns {Array<{ name: string, category: string, tdd_first: boolean, description: string }>}
 */
export function listAllSkills() {
    const index = loadIndex();
    return Object.entries(index).map(([name, meta]) => ({ name, ...meta }));
}
