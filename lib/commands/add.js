// lib/commands/add.js
// Full workflow for: skills add <skill-name> [--force]
//
// Steps:
//   1. Scan Unity project   → ContextReport
//   2. Resolve skill meta   → skills-index.json
//   3. Fetch SKILL.md       → parse YAML frontmatter
//   4. Validate Tier 1 gate → hard-block or warn
//   5. Confirm with user    → prompts
//   6. Install              → Assets/Plugins/AntiGravitySkills/<name>/ (or ~/.antigravity/skills/<name>/)

import os from 'node:os';
import path from 'node:path';

import prompts from 'prompts';
import {
    log,
    spinner,
    printHeader,
} from '../utils/logger.js';
import { scanProject } from '../core/scanner.js';
import { parseFrontmatter } from '../core/yaml-parser.js';
import { validateRequirements } from '../core/validator.js';
import {
    resolveSkillMeta,
    fetchSkillContent,
    listTemplateFiles,
} from '../core/fetcher.js';
import { installSkill, isAlreadyInstalled } from '../core/installer.js';

/**
 * @param {string}  skillName
 * @param {{ force?: boolean, global?: boolean }} opts
 */
export async function addSkill(skillName, opts = {}) {
    printHeader();

    // ── 1. Scan Unity project (if not global) ──────────────────────────────────
    let ctx = null;
    let spin;

    if (!opts.global) {
        spin = spinner('Scanning Unity project...');
        ctx = scanProject();
        spin.stop();

        if (!ctx) {
            log.error('No Unity project found. Run this command from inside a Unity project folder, or use --global.');
            log.dim('  (Looking for ProjectSettings/ProjectVersion.txt up to 8 levels above cwd)');
            process.exit(1);
        }

        log.success(`Project detected: ${ctx.unityVersion}  |  Pipeline: ${ctx.renderPipeline}`);
        log.dim(`  Root: ${ctx.projectRoot}`);
        log.blank();
    } else {
        log.info('Global installation mode selected. Bypassing Unity project context scans.');
        log.blank();
    }

    // ── 2. Resolve skill ───────────────────────────────────────────────────────
    spin = spinner(`Resolving skill "${skillName}"...`);
    const meta = resolveSkillMeta(skillName);
    spin.stop();

    if (!meta) {
        log.error(`Skill not found: "${skillName}"`);
        log.dim('  Run  skills list  to see all available skills.');
        process.exit(1);
    }

    log.success(`Skill found: ${meta.name}  [${meta.category}]`);

    // ── 3. Fetch & parse SKILL.md ──────────────────────────────────────────────
    spin = spinner('Fetching skill metadata...');
    let skillContent;
    try {
        skillContent = await fetchSkillContent(meta);
    } catch (err) {
        spin.stop();
        log.error(`Failed to load skill: ${err.message}`);
        process.exit(1);
    }
    spin.stop();

    const frontmatter = parseFrontmatter(skillContent);
    const requirements = frontmatter?.requirements ?? null;

    // ── 4. Validate Tier 1 gate (skip if global) ───────────────────────────────
    if (!opts.global) {
        spin = spinner('Validating requirements (Tier 1 gate)...');
        const validation = validateRequirements(requirements, ctx);
        spin.stop();

        // Print warnings
        if (validation.warnings.length > 0) {
            log.blank();
            log.warn('Compatibility warnings:');
            for (const w of validation.warnings) log.dim(`  • ${w}`);
        }

        // Hard-block check
        if (validation.hardBlocked) {
            log.blank();
            log.error('Requirements not met — installation blocked:');
            for (const e of validation.errors) log.dim(`  • ${e}`);
            log.blank();

            if (!opts.force) {
                log.warn('Use  --force  to override at your own risk.');
                log.dim('Example: skills add ' + skillName + ' --force');
                process.exit(1);
            }

            log.warn('--force flag detected. Proceeding despite incompatibility. Proceed with caution.');
        } else {
            log.success('All requirements satisfied.');
        }
    }

    // ── 5. Already installed? ──────────────────────────────────────────────────
    if (isAlreadyInstalled(ctx?.projectRoot, meta.name, opts.global) && !opts.force) {
        const { overwrite } = await prompts({
            type: 'confirm',
            name: 'overwrite',
            message: `Skill "${meta.name}" is already installed. Overwrite?`,
            initial: false,
        });
        if (!overwrite) {
            log.info('Installation cancelled.');
            process.exit(0);
        }
    }

    // ── 6. Confirm install ─────────────────────────────────────────────────────
    log.blank();
    const destDir = opts.global
        ? path.join(os.homedir(), '.antigravity', 'skills', meta.name)
        : `Assets/Plugins/AntiGravitySkills/${meta.name}/`;
    log.info(`Ready to install to: ${destDir}`);

    if (!opts.force) {
        const { confirmed } = await prompts({
            type: 'confirm',
            name: 'confirmed',
            message: 'Proceed with installation?',
            initial: true,
        });
        if (!confirmed) {
            log.info('Installation cancelled.');
            process.exit(0);
        }
    }

    // ── 7. Install ─────────────────────────────────────────────────────────────
    spin = spinner('Installing skill...');
    const templateFiles = listTemplateFiles(meta);
    const result = installSkill({
        projectRoot: ctx?.projectRoot,
        skillName: meta.name,
        skillContent,
        templateFiles,
        global: opts.global
    });
    spin.stop();

    log.blank();
    log.success(`✨ Skill "${meta.name}" installed successfully!`);
    log.dim(`  Path: ${result.installedPath}`);
    log.dim(`  Files: ${result.files.length} file(s) copied`);

    if (frontmatter?.tdd_first === false) {
        log.blank();
        log.warn('This is a Standard skill (tdd_first: false). Review generated code carefully.');
    }

    log.blank();
}
