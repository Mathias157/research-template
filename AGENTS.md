# Research Template — Agent Instructions

This is a **reproducible-research project template** that combines:

- **Snakemake** pipeline for data → analysis → report (.tex -> .pdf via latexmk)
- **Conda** environments per pipeline step
- **OpenCode skills** for the LLM-driven research loop
- **Sphinx documentation** for knowledge base and research principles
- **Vault-sync** that mirrors notes from the user's primary Obsidian vault into `docs/.vault-mirror/`
- **Hooks** that auto-track edits, debounce-commit, and emit events

You (the LLM) operate inside this repo. Read this file first, then follow it.

## Repo Layout

```
.
├── .opencode/                  # Skills + sub-agents + commands
│   ├── agent/                  # brainstormer.md, idea-critic.md, research-strategist.md
│   ├── command/                # Optional explicit slash commands
│   ├── skills/                 # research-session, paper-read, lit-search, research-companion,
│   │                           #  weekly-review, orchestrate, vault-sync — each a folder w/ SKILL.md
│   └── AGENTS.md               # Eager-invocation triggers (READ THIS)
│
├── .github/workflows/          # CI: snakemake reproduction, lint
├── hooks/                      # research_hook.sh, auto_commit.sh, vault_sync.sh
│
├── docs/                       # Documentation (Sphinx + principles)
│   ├── principles/             # academic-writing.md, research-strategy.md (referenced by skills)
│   ├── .vault-mirror/          # READ-ONLY mirror from primary Obsidian vault
│   └── (other Sphinx structure)
│
├── # Snakemake side
├── Snakefile                   # The DAG: data -> analysis -> report + tests
├── config/default.yaml         # Pipeline parameters
├── profiles/default/           # Snakemake profile
├── report/                     # LaTeX report (will be compiled to PDF with latexmk)
├── analysis/                   # Analysis scripts, notebooks, or supporting documents
├── tests/                      # Pytest tests of pipeline outputs
├── data/                       # Raw input data (gitkeep)
├── rules/                      # Additional Snakemake rules
│
├── research-state.yaml         # Read on session start (state)
├── events.jsonl                # Append-only event log
├── opencode.json               # OpenCode config (registers hooks)
├── environment.yaml            # Top-level conda env (snakemake)
├── setup.sh                    # Init wizard for customising the template
├── .autocommit.enabled         # Marker (absent by default) — touch to enable auto-commit
└── README.md
```

## Critical Conventions

**LLM agents in this repo are forbidden from running `git commit` under any circumstances.**

The user prefers eager invocation — they don't want to type slash commands.

When their message matches a trigger from `.opencode/AGENTS.md`, IMMEDIATELY READ
the relevant `.opencode/skills/<name>/SKILL.md` and follow it. Do NOT paraphrase
the skill. Do NOT delay with clarifying questions before reading — the skill
itself tells you whether to ask.

Quick reference:

| User says or does... | Read this skill |
|---|---|
| Session start, "what should I work on?", "catch me up" | `research-session` |
| Mentions PDF, arXiv URL, "read this paper", "discuss" | `paper-read` |
| "find papers on X", "lit review", "survey" | `lit-search` |
| "brainstorm", "what if", "should I try X?", proposes an idea | `research-companion` |
| "weekly review", "progress check" | `weekly-review` |
| "sync from vault", "pull notes" | `vault-sync` |
| Multi-angle / complex multi-domain task | `orchestrate` |

### State Discipline

- `research-state.yaml` at repo root — read on session start. The hook updates `last_updated`. You update content fields (`recent_research_evaluations`, `wiki.total_pages`, etc.) as side effects of skill execution.
- `events.jsonl` is **append-only**. Never edit it. Hooks and skills append; nothing rewrites.
- Both files live at the **repo root**, not under `.claude/` or `.opencode/`. This keeps them brand-neutral and visible.

### Documentation Discipline

Research documentation lives in `docs/principles/` and project notes can be synced via vault-sync into `docs/.vault-mirror/`:

- Keep principles in `docs/principles/*.md`
- Vault-sync mirrors project notes into `docs/.vault-mirror/` (read-only input material)
- **Never edit files inside `docs/.vault-mirror/`.** Any edits are overwritten on sync. Use it as input: grep for keywords, cite findings in docs pages.
- Store research data/scripts in Snakemake pipeline
- If user wants content reflected back in primary vault, they edit primary vault directly.

### Hook Awareness

`hooks/research_hook.sh` fires on file writes (configured in `opencode.json`).
It:

- Appends events to `events.jsonl` based on the modified file's path
- Updates `last_updated` in `research-state.yaml`

The hook tracks but does **not** commit. Commits are exclusively the user's responsibility — agents never call `git commit`.

### Principles

Two principle files live at `docs/principles/`:

- **`academic-writing.md`** — 30 prose-quality principles (referenced by paper-read, orchestrate, anything writing-adjacent).
- **`research-strategy.md`** — 8 Carlini-derived strategy principles (referenced by idea-critic, research-strategist, research-companion).

Skills load these by reading the file directly (no plugin needed). When a skill says "see docs/principles/X.md", actually read it.

## Tone & Style

- Match the user's language — Danish or English, mixed is fine.
- The user is doing PhD-level research (energy systems, sector coupling, Balmorel/Antares modelling). Don't condense into pop-science.
- Honest assessments matter more than encouragement. If a paper is weak, say so. If an idea has scooping risk, name names.

## On Skills That Don't Exist Yet

This template provides 7 skills. If the user asks for something that maps to
one of them, use it. If they ask for something that doesn't (e.g., a writing
review pipeline), say so honestly and offer to do it ad-hoc rather than
fabricating a missing skill.

## When in Doubt

1. Read the relevant skill SKILL.md file.
2. Read the principles (`docs/principles/research-strategy.md`, `docs/principles/academic-writing.md`).
3. Read the documentation in `docs/`.
4. Ask the user one specific question, not five.
