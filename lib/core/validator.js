// lib/core/validator.js
// Tier 1 Gate: validates a skill's requirements against the project's ContextReport.
// Returns a structured result the CLI uses to either proceed, warn, or hard-block.

import { parseVersionRequirement } from './yaml-parser.js';
import { parseUnityMajor } from './scanner.js';

const RP_COMPATIBLE = {
    Any: ['URP', 'HDRP', 'BiRP'],
    URP: ['URP'],
    HDRP: ['HDRP'],
    BiRP: ['BiRP'],
};

/**
 * @typedef {Object} ValidationResult
 * @property {boolean}  passed        - Whether the skill can be installed as-is
 * @property {boolean}  hardBlocked   - If true, agent must stop unless user passes --force
 * @property {string[]} errors        - Hard-blocking issues
 * @property {string[]} warnings      - Non-blocking issues (user confirmed)
 */

/**
 * Validate a skill's YAML requirements against the detected ContextReport.
 *
 * @param {object} requirements   - Parsed from SKILL.md YAML (requirements: block)
 * @param {object} contextReport  - From scanner.scanProject()
 * @returns {ValidationResult}
 */
export function validateRequirements(requirements, contextReport) {
    const errors = [];
    const warnings = [];

    if (!requirements) {
        warnings.push('Skill has no requirements block — assuming compatible (legacy skill).');
        return { passed: true, hardBlocked: false, errors, warnings };
    }

    // --- Unity Version Check ---
    if (requirements.unity_version) {
        const minMajor = parseVersionRequirement(requirements.unity_version);
        const projectMajor = parseUnityMajor(contextReport.unityVersion);

        if (projectMajor < minMajor) {
            errors.push(
                `Unity version mismatch: skill requires ${requirements.unity_version}, ` +
                `project has ${contextReport.unityVersion}.`
            );
        }
    }

    // --- Render Pipeline Check ---
    const rpReq = requirements.render_pipeline;
    if (rpReq && rpReq !== 'Any') {
        const allowed = RP_COMPATIBLE[rpReq] ?? [rpReq];
        if (!allowed.includes(contextReport.renderPipeline)) {
            errors.push(
                `Render pipeline mismatch: skill requires ${rpReq}, ` +
                `project uses ${contextReport.renderPipeline}.`
            );
        }
    }

    // --- Package Dependency Check ---
    const deps = requirements.dependencies ?? [];
    for (const dep of deps) {
        const cleanDep = dep.replace(/^["']|["']$/g, ''); // strip quotes if any
        if (!contextReport.packages.some(p => p.startsWith(cleanDep))) {
            warnings.push(`Missing package: ${cleanDep} — add it via Package Manager before using this skill.`);
        }
    }

    const hardBlocked = errors.length > 0;
    return {
        passed: !hardBlocked,
        hardBlocked,
        errors,
        warnings,
    };
}
