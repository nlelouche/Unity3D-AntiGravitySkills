#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { parseFrontmatter } from '../lib/core/yaml-parser.js';
import { validateRequirements } from '../lib/core/validator.js';
import chalk from 'chalk';

console.log(chalk.bold.blue('--- AntiGravity Skills CLI: Automated Test Runner ---'));

let passed = 0;
let failed = 0;

function assert(condition, message) {
    if (condition) {
        passed++;
        console.log(chalk.green('  [PASS] ') + message);
    } else {
        failed++;
        console.error(chalk.red('  [FAIL] ') + message);
    }
}

console.log(chalk.cyan('\n1. Testing YAML Extraction:'));
try {
    const mockMd = `---\nname: test-skill\nversion: 1.0.0\n---\n# Markdown Body\nSome text...`;
    const parsedObj = parseFrontmatter(mockMd);
    assert(parsedObj !== null && parsedObj.name === 'test-skill', 'Should successfully extract and parse YAML frontmatter from Markdown string');
} catch (e) {
    console.error(e);
    assert(false, 'YAML Parser crashed');
}

console.log(chalk.cyan('\n2. Testing Validation Logic (Compatibility Check):'));
try {
    const mockRequirements = {
        unity_version: ">=2021.3",
        render_pipeline: "URP",
        dependencies: ["com.unity.addressables"]
    };

    const validContext = {
        unityVersion: "6000.0.1f1",
        renderPipeline: "URP",
        packages: ["com.unity.addressables", "com.unity.timeline"]
    };

    const missingDepContext = {
        unityVersion: "6000.0.1f1",
        renderPipeline: "URP",
        packages: []
    };

    const wrongPipelinContext = {
        unityVersion: "6000.0.1f1",
        renderPipeline: "HDRP",
        packages: ["com.unity.addressables"]
    };

    // Valid check
    const validResult = validateRequirements(mockRequirements, validContext);
    assert(validResult.passed === true, 'Validation passes when all requirements are met');
    assert(validResult.warnings.length === 0, 'No warnings for perfectly matching context');

    // Missing dependencies check
    const missingResult = validateRequirements(mockRequirements, missingDepContext);
    assert(missingResult.warnings.some(w => w.includes('addressables')), 'Validation correctly flags missing unity packages');

    // Display pipeline check
    const rpResult = validateRequirements(mockRequirements, wrongPipelinContext);
    assert(rpResult.errors.some(e => e.includes('Render pipeline mismatch')), 'Validation correctly flags mismatching render pipeline');

} catch (e) {
    console.error(e);
    assert(false, 'Validator tests crashed');
}

console.log(chalk.cyan('\n3. Testing Skill File Integrity:'));
try {
    const skillsDir = path.resolve(process.cwd(), '.agent/skills');
    if (fs.existsSync(skillsDir)) {
        assert(true, 'Skills repository detected. Checking SKILL.md structure...');
        const categories = fs.readdirSync(skillsDir).filter(dir => fs.statSync(path.join(skillsDir, dir)).isDirectory());
        let count = 0;
        let missing = 0;
        for (const cat of categories) {
            const skills = fs.readdirSync(path.join(skillsDir, cat)).filter(dir => fs.statSync(path.join(skillsDir, cat, dir)).isDirectory());
            for (const skill of skills) {
                const skillPath = path.join(skillsDir, cat, skill, 'SKILL.md');
                if (fs.existsSync(skillPath)) {
                    count++;
                } else {
                    missing++;
                }
            }
        }
        assert(missing === 0, `All skills have SKILL.md (${count} found, ${missing} missing)`);
    } else {
        console.warn(chalk.yellow('  [SKIP] No skills directory found locally to test integrity.'));
    }
} catch (e) {
    assert(false, 'Integrity test crashed');
}

console.log('\n--- Test Summary ---');
console.log(chalk.bold(`Total: ${passed + failed} | ` + chalk.green(`Pass: ${passed}`) + ' | ' + chalk.red(`Fail: ${failed}`)));

if (failed > 0) {
    process.exit(1);
} else {
    process.exit(0);
}
