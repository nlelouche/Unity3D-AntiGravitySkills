// lib/commands/list.js
// skills list             — all skills, grouped by category
// skills list --category performance
// skills list --tdd       — show only TDD-native skills

import chalk from 'chalk';
import { log, printHeader } from '../utils/logger.js';
import { listAllSkills } from '../core/fetcher.js';

const CATEGORY_LABELS = {
    '00-core-engineering': '⚙️  Core Engineering',
    '00-meta-skills': '🧠 Meta Skills',
    '01-architecture': '🏛  Architecture',
    '02-gameplay': '🎮 Gameplay',
    '03-simulation-strategy': '🎯 Simulation & Strategy',
    '04-visuals-audio': '🎨 Visuals & Audio',
    '05-ui-ux': '🖥️  UI/UX',
    '06-performance': '⚡ Performance',
    '07-tools-pipeline': '🛠️  Tools & Pipeline',
    '08-backend-monetization': '💰 Backend & Monetization',
    '09-devops-automation': '🚀 DevOps & Automation',
};

/**
 * @param {{ category?: string, tdd?: boolean }} opts
 */
export function listSkills(opts = {}) {
    printHeader();

    let skills = listAllSkills();

    // Filter by category
    if (opts.category) {
        const filter = opts.category.toLowerCase();
        skills = skills.filter(s =>
            s.category.toLowerCase().includes(filter) ||
            (CATEGORY_LABELS[s.category] ?? '').toLowerCase().includes(filter)
        );
    }

    // Filter TDD-only
    if (opts.tdd) {
        skills = skills.filter(s => s.tdd_first === true);
    }

    if (skills.length === 0) {
        log.warn('No skills match the given filters.');
        return;
    }

    // Group by category
    const byCategory = {};
    for (const skill of skills) {
        (byCategory[skill.category] ??= []).push(skill);
    }

    let total = 0;
    for (const [cat, catSkills] of Object.entries(byCategory).sort()) {
        const label = CATEGORY_LABELS[cat] ?? cat;
        console.log(chalk.bold.magenta(`\n  ${label}`));
        console.log(chalk.dim('  ' + '─'.repeat(62)));

        for (const s of catSkills.sort((a, b) => a.name.localeCompare(b.name))) {
            const tag = s.tdd_first ? chalk.green('⭐ TDD   ') : chalk.yellow('🔧 Standard');
            const name = chalk.white(s.name.padEnd(42));
            const desc = chalk.dim((s.description ?? '').slice(0, 55));
            console.log(`  ${tag}  ${name}  ${desc}`);
            total++;
        }
    }

    console.log(chalk.dim(`\n  ${'─'.repeat(66)}`));
    console.log(`  ${chalk.cyan(total)} skill${total !== 1 ? 's' : ''} found`);

    if (opts.tdd) {
        console.log(chalk.dim('  (Showing TDD-native skills only. Remove --tdd to see all.)'));
    }

    log.blank();
    log.dim('  Install any skill with:  npx github:nlelouche/Unity-SkillForge add <skill-name>');
    log.blank();
}
