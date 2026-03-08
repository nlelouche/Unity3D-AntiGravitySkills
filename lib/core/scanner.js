// lib/core/scanner.js
// Walks up from cwd to find a Unity project root, then reads:
//   ProjectSettings/ProjectVersion.txt  → unity version
//   Packages/manifest.json              → installed packages + render pipeline

import fs from 'node:fs';
import path from 'node:path';

const RP_MAP = {
    'com.unity.render-pipelines.universal': 'URP',
    'com.unity.render-pipelines.high-definition': 'HDRP',
};

/**
 * Walk up from startDir looking for ProjectSettings/ProjectVersion.txt
 * @param {string} startDir
 * @returns {string|null} project root or null
 */
function findUnityRoot(startDir) {
    let dir = startDir;
    for (let i = 0; i < 8; i++) {          // max 8 levels up
        const candidate = path.join(dir, 'ProjectSettings', 'ProjectVersion.txt');
        if (fs.existsSync(candidate)) return dir;
        const parent = path.dirname(dir);
        if (parent === dir) break;            // filesystem root
        dir = parent;
    }
    return null;
}

/**
 * Parse ProjectVersion.txt and return the editor version string (e.g. "6000.1.2f1")
 */
function parseUnityVersion(projectRoot) {
    const filePath = path.join(projectRoot, 'ProjectSettings', 'ProjectVersion.txt');
    const raw = fs.readFileSync(filePath, 'utf8');
    const match = raw.match(/m_EditorVersion:\s*(\S+)/);
    return match ? match[1] : 'unknown';
}

/**
 * Parse Packages/manifest.json and return installed package names + detected RP
 */
function parseManifest(projectRoot) {
    const filePath = path.join(projectRoot, 'Packages', 'manifest.json');
    if (!fs.existsSync(filePath)) return { packages: [], renderPipeline: 'BiRP' };

    const manifest = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const dependencies = manifest.dependencies ?? {};
    const packages = Object.keys(dependencies);

    let renderPipeline = 'BiRP';
    for (const [pkg, rp] of Object.entries(RP_MAP)) {
        if (pkg in dependencies) { renderPipeline = rp; break; }
    }

    return { packages, renderPipeline };
}

/**
 * Scan the current Unity project and produce a ContextReport
 * @param {string} [startDir=process.cwd()]
 * @returns {{ projectRoot: string, unityVersion: string, renderPipeline: string, packages: string[] }|null}
 */
export function scanProject(startDir = process.cwd()) {
    const projectRoot = findUnityRoot(startDir);
    if (!projectRoot) return null;

    const unityVersion = parseUnityVersion(projectRoot);
    const { packages, renderPipeline } = parseManifest(projectRoot);

    return { projectRoot, unityVersion, renderPipeline, packages };
}

/**
 * Parse a semver-like Unity version string into a comparable number.
 * "6000.1.2f1" → 6000.001002  (major * 1000 + minor * 0.001 ...)
 * Simplified: just returns the major version number.
 */
export function parseUnityMajor(versionStr) {
    const m = versionStr.match(/^(\d+)/);
    return m ? parseInt(m[1], 10) : 0;
}
