#!/bin/bash

# AntiGravity Setup Script for macOS/Linux
# Usage: ./setup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Initializing AntiGravity Skills from: $SCRIPT_DIR"

# Determine Project Root (Assuming .agent/antigravity structure)
PROJECT_ROOT="$SCRIPT_DIR/../.."

# Basic check for Unity structure
if [ -d "$PROJECT_ROOT/Assets" ] || [ -d "$PROJECT_ROOT/ProjectSettings" ]; then
    echo "[+] Project Root detected at: $PROJECT_ROOT"
else
    echo "[!] Warning: Could not detect standard Unity project structure at $PROJECT_ROOT"
    echo "    Proceeding assuming this is the target root."
fi

# --- 1. Setup AGENT.md ---
SOURCE_AGENT_MD="$SCRIPT_DIR/AGENT.md"
TARGET_AGENT_MD="$PROJECT_ROOT/AGENT.md"

if [ -f "$SOURCE_AGENT_MD" ]; then
    if [ ! -f "$TARGET_AGENT_MD" ]; then
        cp "$SOURCE_AGENT_MD" "$TARGET_AGENT_MD"
        echo "[+] Copied AGENT.md to Project Root."
    else
        echo "[-] AGENT.md already exists in Project Root. Skipping."
    fi
else
    echo "[!] Error: Source AGENT.md not found in $SCRIPT_DIR"
fi

# --- 2. Setup .agent/skills Symlink ---
SOURCE_SKILLS_DIR="$SCRIPT_DIR/.agent/skills"
TARGET_AGENT_DIR="$PROJECT_ROOT/.agent"
TARGET_SKILLS_DIR="$TARGET_AGENT_DIR/skills"

# Ensure .agent folder exists
if [ ! -d "$TARGET_AGENT_DIR" ]; then
    mkdir -p "$TARGET_AGENT_DIR"
    echo "[+] Created '$TARGET_AGENT_DIR' directory."
fi

# Create Soft Link
if [ -e "$TARGET_SKILLS_DIR" ]; then
    echo "[-] '$TARGET_SKILLS_DIR' already exists. Skipping link creation."
else
    if [ -d "$SOURCE_SKILLS_DIR" ]; then
        ln -s "$SOURCE_SKILLS_DIR" "$TARGET_SKILLS_DIR"
        echo "[+] Created Symlink: $TARGET_SKILLS_DIR -> $SOURCE_SKILLS_DIR"
    else
        echo "[!] Error: Skills source directory not found at $SOURCE_SKILLS_DIR"
    fi
fi

echo -e "\nAntiGravity Setup Complete! 🚀"
