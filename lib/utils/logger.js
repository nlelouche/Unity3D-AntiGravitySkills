// lib/utils/logger.js
import chalk from 'chalk';
import ora from 'ora';

const icons = {
    info: chalk.cyan('ℹ'),
    success: chalk.green('✔'),
    warn: chalk.yellow('⚠'),
    error: chalk.red('✖'),
    skill: chalk.magenta('◆'),
    tdd: chalk.green('⭐'),
    legacy: chalk.yellow('🔧'),
};

export const log = {
    info: (msg) => console.log(`${icons.info}  ${chalk.cyan(msg)}`),
    success: (msg) => console.log(`${icons.success}  ${chalk.green(msg)}`),
    warn: (msg) => console.log(`${icons.warn}  ${chalk.yellow(msg)}`),
    error: (msg) => console.error(`${icons.error}  ${chalk.red(msg)}`),
    dim: (msg) => console.log(chalk.dim(msg)),
    blank: () => console.log(),
};

export function spinner(text) {
    return ora({ text: chalk.cyan(text), spinner: 'dots' }).start();
}

export function printHeader() {
    console.log(chalk.magenta.bold('\n  🌌 AntiGravity Skills CLI — v2.0.0'));
    console.log(chalk.dim('  Zero-lock-in Unity skill installer\n'));
}

export function printSkillRow(name, meta) {
    const tag = meta.tdd_first
        ? chalk.green('⭐ TDD')
        : chalk.yellow('🔧 Legacy');
    const cat = chalk.dim(meta.category.replace(/^\d{2}-/, ''));
    const desc = chalk.white(meta.description?.slice(0, 72) ?? '');
    console.log(`  ${chalk.magenta(name.padEnd(40))} ${tag.padEnd(20)} ${cat}`);
    if (desc) console.log(`    ${chalk.dim(desc)}`);
}
