// lib/commands/add-all.js
// skills add-all [--force]
// Installs all skills and optionally injects AGENT.md

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import prompts from 'prompts';
import { log, spinner, printHeader } from '../utils/logger.js';
import { scanProject } from '../core/scanner.js';
import { listAllSkills, fetchSkillContent, listTemplateFiles } from '../core/fetcher.js';
import { installSkill } from '../core/installer.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '../../');
const AGENT_SRC = path.join(REPO_ROOT, 'AGENT.md');

/**
 * @param {{ force?: boolean, global?: boolean }} opts
 */
export async function addAllSkills(opts = {}) {
    printHeader();

    // 1. Scan Unity project (if not global)
    let ctx = null;
    let spin;

    if (!opts.global) {
        spin = spinner('Scanning Unity project...');
        ctx = scanProject();
        spin.stop();

        if (!ctx) {
            log.error('No Unity project found. Run this command from inside a Unity project folder, or use --global.');
            process.exit(1);
        }

        log.success(`Project detected: ${ctx.unityVersion}  |  Pipeline: ${ctx.renderPipeline}`);
        log.blank();
    } else {
        log.info('Global installation mode selected. Bypassing Unity project context scans.');
        log.blank();
    }

    const skills = listAllSkills();

    // 2. Prompt for confirmation
    if (!opts.force) {
        const { confirmed } = await prompts({
            type: 'confirm',
            name: 'confirmed',
            message: `Are you sure you want to install ALL ${skills.length} skills into this project?`,
            initial: false,
        });
        if (!confirmed) {
            log.info('Installation cancelled.');
            process.exit(0);
        }
    }

    // 3. Optional AGENT.md injection
    let installAgent = true;
    if (!opts.force) {
        const response = await prompts({
            type: 'confirm',
            name: 'installAgent',
            message: 'Do you also want to inject the AntiGravity Architect Persona (AGENT.md)?',
            initial: true,
        });
        installAgent = response.installAgent;
    }

    if (installAgent) {
        if (!fs.existsSync(AGENT_SRC)) {
            log.warn(`Could not locate AGENT.md source at ${AGENT_SRC}`);
        } else {
            const personaContent = fs.readFileSync(AGENT_SRC, 'utf8');
            let destPaths;

            if (opts.global) {
                destPaths = [path.join(os.homedir(), '.antigravity', 'AGENT.md')];
            } else {
                destPaths = [
                    path.join(ctx.projectRoot, '.cursorrules'),
                    path.join(ctx.projectRoot, '.agent/AGENT.md')
                ];
            }

            for (const destPath of destPaths) {
                const destDir = path.dirname(destPath);
                if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
                fs.writeFileSync(destPath, personaContent, 'utf8');
                if (opts.global) {
                    log.dim(`  + Wrote ${destPath}`);
                } else {
                    log.dim(`  + Wrote ${path.relative(ctx.projectRoot, destPath)}`);
                }
            }
            log.success('🧠 Architect Persona injected successfully.');
            log.blank();
        }
    }

    // 4. Install all skills
    log.info(`Installing ${skills.length} skills... This might take a moment.`);
    let installedCount = 0;
    let failedCount = 0;

    for (const meta of skills) {
        try {
            const skillContent = await fetchSkillContent(meta);
            const templateFiles = listTemplateFiles(meta);
            installSkill({
                projectRoot: ctx?.projectRoot,
                skillName: meta.name,
                skillContent,
                templateFiles,
                global: opts.global
            });
            installedCount++;
            process.stdout.write(`\rInstalled ${installedCount}/${skills.length} skills...`);
        } catch (err) {
            failedCount++;
        }
    }

    console.log(); // New line after progress
    log.blank();
    log.success(`✨ Installed ${installedCount} skills successfully.`);
    if (failedCount > 0) {
        log.warn(`⚠ Failed to install ${failedCount} skills.`);
    }
    log.blank();
}
