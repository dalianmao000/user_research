# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

User Research AI Agents System - a Claude Code Skills + Obsidian + Docker based automation system for user research workflows including interview analysis, insight extraction, PRD generation, and report writing.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (11 tests, all passing)
python3 -m pytest tests/ -v

# Run a single test
python3 -m pytest tests/test_obsidian_sync.py::TestObsidianSync::test_init_creates_vault_structure -v

# Initialize Obsidian Vault
python3 scripts/obsidian-sync.py init

# Docker services (requires Docker Desktop)
cd docker && docker-compose up -d
# n8n UI: http://localhost:5678
# Weaviate: http://localhost:8080
# PostgreSQL: localhost:5432

# Code formatting
pip install black ruff
black .
ruff check .
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Claude Code (Skills)               │
│  /ur-start, /ur-interview, /ur-requirements   │
├─────────────────────────────────────────────────┤
│                 Obsidian                        │
│     Knowledge base / Note management / RAG     │
├─────────────────────────────────────────────────┤
│              Docker Services                    │
│   n8n (workflow) │ Weaviate (vectors) │ PostgreSQL │
└─────────────────────────────────────────────────┘
```

### Skills System (`skills/`)
- `skills/skill.json` - Skill metadata with 7 commands
- `skills/user-research/skill.md` - Main skill entry point
- `skills/user-research/agents/` - 5 AI Agents (markdown prompt files):
  - `data-fusion.md` - Interview analysis, insight extraction
  - `full-cycle-ur.md` - PRD generation from insights
  - `global-insight.md` - Report generation
  - `process-orchestrate.md` - Workflow coordination
  - `compliance.md` - Privacy/compliance
- `skills/user-research/prompts/` - Prompt templates

### Obsidian Vault (`obsidian-vault/`)
Standard directory structure for user research:
- `00-项目/` - Project docs
- `01-用户访谈/` - Raw interview records
- `02-洞察笔记/` - Analyzed insights
- `03-需求池/` - PRD drafts
- `04-报告/` - Final reports

### ObsidianSync Tool (`scripts/obsidian-sync.py`)
Python class with methods: `init()`, `add_note()`, `search_notes()`, `index`, `generate_daily_note()`, `export_index()`, `backup()`, `sync()`

### Docker Services
- **n8n** (port 5678) - Workflow automation
- **Weaviate** (port 8080) - Vector database for semantic search
- **PostgreSQL** (port 5432) - Structured data storage

## Key Notes

- Agents are defined as markdown prompt files, not Python code
- Tests use pytest and mock the actual ObsidianSync module via `importlib.util`
- Skills are installed by copying `skills/*` to `~/.claude/skills/`
- Docker services are optional - core functionality works without them