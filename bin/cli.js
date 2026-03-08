#!/usr/bin/env node
// bin/cli.js — AntiGravity Skills CLI entry point
// Usage:
//   npx @antigravity/skills list [--category <cat>] [--tdd]
//   npx @antigravity/skills add <skill-name> [--force]

import { program } from 'commander';
import { addSkill } from '../lib/commands/add.js';
import { listSkills } from '../lib/commands/list.js';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgPath = path.join(__dirname, '..', 'package.json');
const { version } = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));

program
    .name('skills')
    .description('AntiGravity Skills CLI — zero-lock-in Unity skill installer')
    .version(version);

// ── skills list ───────────────────────────────────────────────────────────────
program
    .command('list')
    .description('List all available skills grouped by category')
    .option('-c, --category <name>', 'Filter by category (e.g. performance, ui-ux)')
    .option('--tdd', 'Show only TDD-native skills (tdd_first: true)')
    .action((opts) => {
        listSkills({ category: opts.category, tdd: opts.tdd });
    });

// ── skills add <name> ─────────────────────────────────────────────────────────
program
    .command('add <skill-name>')
    .description('Install a skill into the current Unity project')
    .option('-f, --force', 'Override requirement failures and skip confirmations')
    .action(async (skillName, opts) => {
        try {
            await addSkill(skillName, { force: opts.force });
        } catch (err) {
            console.error('\n  ✖  Unexpected error:', err.message);
            process.exit(1);
        }
    });

// ── skills info <name> ────────────────────────────────────────────────────────
program
    .command('info <skill-name>')
    .description('Show metadata and requirements for a skill without installing')
    .action(async (skillName) => {
        const { resolveSkillMeta, fetchSkillContent } = await import('../lib/core/fetcher.js');
        const { parseFrontmatter } = await import('../lib/core/yaml-parser.js');
        const { log, printHeader } = await import('../lib/utils/logger.js');
        const chalk = (await import('chalk')).default;

        printHeader();
        const meta = resolveSkillMeta(skillName);
        if (!meta) {
            log.error(`Skill not found: "${skillName}". Run  skills list  to browse available skills.`);
            process.exit(1);
        }

        const content = await fetchSkillContent(meta);
        const fm = parseFrontmatter(content);

        console.log(chalk.bold.magenta(`\n  ${meta.name}`));
        console.log(chalk.dim(`  ${meta.description ?? ''}\n`));
        console.log(`  Category   : ${chalk.cyan(meta.category)}`);
        console.log(`  Version    : ${chalk.white(fm?.version ?? 'N/A')}`);
        console.log(`  TDD-First  : ${fm?.tdd_first ? chalk.green('✔ true') : chalk.yellow('✖ false (Legacy)')}`);

        if (fm?.requirements) {
            console.log(`\n  Requirements:`);
            console.log(`    Unity    : ${chalk.white(fm.requirements.unity_version ?? 'Any')}`);
            console.log(`    Pipeline : ${chalk.white(fm.requirements.render_pipeline ?? 'Any')}`);
            const deps = fm.requirements.dependencies ?? [];
            if (deps.length)
                console.log(`    Packages : ${chalk.white(deps.join(', '))}`);
        }

        if (fm?.performance_budget) {
            console.log(`\n  Performance Budget:`);
            console.log(`    GC/frame : ${chalk.white(fm.performance_budget.gc_alloc_per_frame)}`);
            console.log(`    Update   : ${chalk.white(fm.performance_budget.max_update_cost)}`);
        }
        console.log();
    });

// ── skills init ───────────────────────────────────────────────────────────────
program
    .command('init')
    .description('Inject the AntiGravity Architect persona into this project')
    .action(async () => {
        try {
            const { initAgent } = await import('../lib/commands/init.js');
            await initAgent();
        } catch (err) {
            console.error('\n  ✖  Unexpected error:', err.message);
            process.exit(1);
        }
    });

program.parse();
