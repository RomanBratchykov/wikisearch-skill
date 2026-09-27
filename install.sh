#!/usr/bin/env bash
set -e

SKILL_DIR="$HOME/.claude/skills/wikisearch"

git clone https://github.com/RomanBratchykov/wikisearch-skill.git "$SKILL_DIR"

cd "$SKILL_DIR"
uv sync
