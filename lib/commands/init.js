// lib/commands/init.js
// skills init
// Injects the AGENT.md persona into the local Unity project to activate the Tech Lead.
// Copies to .agent/AGENT.md and/or .cursorrules (for Cursor users).

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import prompts from 'prompts';
import { log, spinner, printHeader } from '../utils/logger.js';
import { scanProject } from '../core/scanner.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '../../');
const AGENT_SRC = path.join(REPO_ROOT, 'AGENT.md');

export async function initAgent() {
    printHeader();

    const spin = spinner('Scanning project...');
    const ctx = scanProject();
    spin.stop();

    if (!ctx) {
        log.error('No Unity project found. Please run this command from the root of a Unity project.');
        process.exit(1);
    }

    log.success(`Unity project detected at: ${ctx.projectRoot}`);
    log.blank();

    if (!fs.existsSync(AGENT_SRC)) {
        // If installed globally via npm, reaching the parent AGENT.md depends on package structure.
        // Assuming AGENT.md is published alongside bin/ and lib/
        log.error(`Could not locate AGENT.md source at ${AGENT_SRC}`);
        process.exit(1);
    }

    const personaContent = fs.readFileSync(AGENT_SRC, 'utf8');

    // We offer two installation targets: .cursorrules (for Cursor) or .agent/AGENT.md (standard)
    const { targets } = await prompts({
        type: 'multiselect',
        name: 'targets',
        message: 'Where should we install the Architect Persona?',
        choices: [
            { title: '.cursorrules (Recommended for Cursor AI)', value: '.cursorrules', selected: true },
            { title: '.agent/AGENT.md (Standard / Other AIs)', value: '.agent/AGENT.md' },
        ],
        min: 1
    });

    if (!targets) {
        log.info('Cancelled.');
        process.exit(0);
    }

    log.blank();
    const installSpin = spinner('Injecting AntiGravity Architect Persona...');

    for (const target of targets) {
        const destPath = path.join(ctx.projectRoot, target);
        const destDir = path.dirname(destPath);

        if (!fs.existsSync(destDir)) {
            fs.mkdirSync(destDir, { recursive: true });
        }

        fs.writeFileSync(destPath, personaContent, 'utf8');
        log.dim(`  + Wrote ${target}`);
    }

    installSpin.stop();
    log.blank();
    log.success('🧠 Architect Persona successfully injected!');
    log.dim('  Your AI assistant will now act as a Senior Tech Lead.');
    log.dim('  It will prevent Vibe Coding and enforce ZERO-GC / TDD standards.');
    log.blank();
}
