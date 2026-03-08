// lib/core/yaml-parser.js
// Lightweight YAML frontmatter extractor — no dependencies beyond js-yaml.
// Parses the --- block at the top of SKILL.md files.

import yaml from 'js-yaml';

/**
 * Extract and parse the YAML frontmatter from a SKILL.md string.
 * Returns the parsed object or null if no frontmatter is found.
 * @param {string} content - Full SKILL.md file content
 * @returns {object|null}
 */
export function parseFrontmatter(content) {
    const FM_REGEX = /^---\r?\n([\s\S]*?)\r?\n---/;
    const match = content.match(FM_REGEX);
    if (!match) return null;

    try {
        return yaml.load(match[1]);
    } catch {
        return null;
    }
}

/**
 * Parse a Unity version requirement string like ">=6.0" and return
 * the numeric minimum major version.
 * @param {string} req  e.g. ">=6.0" | ">=2022.3"
 * @returns {number}
 */
export function parseVersionRequirement(req) {
    if (!req) return 0;
    const m = req.match(/(\d+)/);
    return m ? parseInt(m[1], 10) : 0;
}
