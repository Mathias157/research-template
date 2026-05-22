# Research Template

A reproducible-research project template combining Snakemake pipeline, Sphinx documentation, and an LLM-driven research loop.

It integrates structures from three repositories:

1. **A working pipeline** — Snakemake DAG, Pixi environment management, LaTeX-compiled PDF report, pytest, GitHub Actions CI/CD that re-runs every push. Adapted from [timtroendle/cookiecutter-reproducible-research](https://github.com/timtroendle/cookiecutter-reproducible-research) with some inspiration from [FedericoTartarini/reproducible-research](https://github.com/FedericoTartarini/reproducible-research).
2. **Documentation system** — Sphinx-based documentation with research principles (`docs/principles/`), vault sync target (`docs/.vault-mirror/`), and structured knowledge base.
3. **An LLM research loop** — `paper-read`, `lit-search`, `research-companion`, `weekly-review`, `orchestrate`, `vault-sync` skills with eager invocation. Three sub-agents (brainstormer, idea-critic, research-strategist) for divergence, critique, and strategy. Hook-based bookkeeping for event tracking and state management.

The result is one repo where the *thinking* (documentation + skills) and the *running* (Snakemake + tests) sit next to each other and don't drift.

## What you get

```
.
├── .opencode/                  # Skills + sub-agents (eager invocation)
│   ├── agent/                  # brainstormer, idea-critic, research-strategist
│   └── skills/                 # 7 skills covering the full research loop
├── .github/workflows/          # reproduction.yaml + lint.yaml
├── hooks/                      # research_hook.sh, vault_sync.sh
├── docs/                       # Documentation (Sphinx + principles)
│   ├── principles/             # academic-writing.md, research-strategy.md
│   └── .vault-mirror/          # READ-ONLY mirror of primary Obsidian vault
├── Snakefile + analysis/ + tests/ + report/
├── pixi.toml                   # Pixi environment
├── research-state.yaml         # State (read on session start)
└── events.jsonl                # Append-only event log
```

## The Loop

```
                   ┌──────────────────────┐
                   │  research-session    │  ← eager-invoked on greetings
                   │  (briefing + route)  │
                   └──────────┬───────────┘
                              ▼
    ┌─────────────┬───────────────────┬───────────────┐
    │ paper-read  │ research-companion│  lit-search   │
    │  (5 phases) │   (6 phases)      │  (subfield    │
    │             │  brainstormer +   │   workspace)  │
    │             │  idea-critic +    │               │
    │             │  research-strategist              │
    └──────┬──────┴─────────┬─────────┴───────┬───────┘
           ▼                ▼                 ▼
        docs/topics     docs/research-      docs/queries
        docs/entities   evaluations         (graduates →
                                             topics/syntheses)

     weekly-review reads events.jsonl + state + git log
      vault-sync mirrors primary vault → docs/.vault-mirror/
      research_hook.sh logs every write
```

## Eager Invocation

Skills are not slash commands. The LLM detects intent and reads the relevant SKILL.md. See `.opencode/AGENTS.md` for the full trigger table; the short version:

| You say... | LLM activates |
|---|---|
| "what should I work on?", "catch me up", session start | `research-session` |
| Mentions a PDF, arXiv URL, "read this paper" | `paper-read` |
| "find papers on X", "lit review", "survey [field]" | `lit-search` |
| "brainstorm", "what if", "should I try X?" | `research-companion` |
| "weekly review", "progress check" | `weekly-review` |
| "sync from vault", "pull notes" | `vault-sync` |
| Multi-angle / parallel review | `orchestrate` |

## Philosophy

Research lives in the handoffs between activities. Reading on Monday, drafting on Friday, brainstorming in between — without a binding substrate, none of those activities know the others happened. This template gives you that substrate as plain text the machine maintains for you.

The hook is non-negotiable: humans abandon knowledge bases because maintaining cross-references is boring; LLMs don't get bored. Documentation is the system of record; everything else (state file, event log, primary vault) feeds it.

```{toctree}
:maxdepth: 1

principles
other
developing
about
```
