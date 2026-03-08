# AntiGravity Skills CLI Spec (2.0.0)

This document serves as the high-level architecture and design specification for the `skills` CLI wrapper leveraging `npx` built purely for the AntiGravity Architect methodology.

## Philosophy
The goal is **Zero Lock-In**. The CLI acts purely as an injector (scaffolder). It copies self-contained, high-quality script files directly into the target project via `npx`, avoiding package manager clutter, strict NPM resolutions, or hidden dependencies inside `Library/PackageCache`. The developer gets raw, editable C# files.

## High Level Use Cases
- **Discovery**: `npx github:... list` allows an agent or human to find the skill they are looking for.
- **Validation**: `npx github:... info <skill>` parses project settings and confirms Unity 6+, pipeline matching, and required packages for the skill.
- **Installation**: `npx github:... add <skill>` physically copies templates to `Assets/Plugins/AntiGravitySkills/<skill>`.
- **Global / Agent**: `npx github:... init / add-all --global` bootstraps an Agentic workflow directly to the user's OS without polluting a specific Unity project setup.

## Module Architecture
```
bin/
├── cli.js                         # Commander.js entrypoint. Parses args.
lib/
├── commands/
│   ├── add.js                     # Implements `skills add <skill>`
│   ├── add-all.js                 # Implements `skills add-all`
│   ├── init.js                    # Implements `skills init` (AGENT.md injection)
│   └── list.js                    # Implements `skills list`
├── core/
│   ├── fetcher.js                 # Resolves paths / fetches via raw Github URLs
│   ├── installer.js               # Cross-platform file copier (`fs`, `os`)
│   ├── scanner.js                 # Extracts Unity context from `ProjectVersion.txt` and `manifest.json`
│   ├── validator.js               # Compares YAML rules vs Unity context
│   └── yaml-parser.js             # Parses YAML `---` frontmatter from Markdown
└── utils/
    └── logger.js                  # Chalk/Ora CLI spinner + coloring
```

## TDD-First Distinction
Skills fall into two distinct badges on the CLI:
1. `⭐ TDD` - Skills natively built under the 2026 specs, guaranteeing zero GC allocations, interfaces, mocking capabilities, and explicit tests.
2. `🔧 Standard` - Legacy solid foundation scripts. Working perfectly, but lacking built-in explicit TDD tests and requiring minor human/AI oversight upon installation.

## Future Plans
- Expanding `add` with `--dry-run` to preview file operations before executing copy.
- NPM publish to `@nlelouche/antigravity` allowing simple `npx @nlelouche/antigravity add ...` usages.
