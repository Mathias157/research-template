# Research Template

A reproducible-research project template combining Snakemake pipeline, Sphinx documentation, and an LLM-driven research loop.

It integrates structures from three repositories:

1. **A working pipeline** — Snakemake DAG, Conda environment management, LaTeX-compiled PDF report, pytest, GitHub Actions CI/CD that re-runs every push. Adapted from [`timtroendle/cookiecutter-reproducible-research`](https://github.com/timtroendle/cookiecutter-reproducible-research) with some inspiration 
from [FedericoTartarini/reproducible-research](https://github.com/FedericoTartarini/reproducible-research).
2. **Documentation system** — Sphinx-based documentation with research principles (`docs/principles/`), vault sync target (`docs/.vault-mirror/`), and structured knowledge base. 
3. **An LLM research loop** — `paper-read`, `lit-search`, `research-companion`, `weekly-review`, `orchestrate`, `vault-sync` skills with eager invocation. Three sub-agents (brainstormer, idea-critic, research-strategist) for divergence, critique, and strategy. Hook-based bookkeeping for event tracking and state management.

The result is one repo where the *thinking* (documentation + skills) and the *running*
(Snakemake + tests) sit next to each other and don't drift.

## Quickstart

```bash
git clone https://github.com/Mathias157/research-template.git my-project
cd my-project
rm -rf .git
./setup.sh                 # interactive wizard: project name, vault sync
pixi install
pixi run snakemake --cores 4        # build the demo report
```

Then open the repo in OpenCode and start a conversation. The
`research-session` skill activates eagerly on greetings, briefings, or "what
should I work on?".

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
├── environment.yaml            # Conda environment
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

Skills are not slash commands. The LLM detects intent and reads the relevant
SKILL.md. See `.opencode/AGENTS.md` for the full trigger table; the short
version:

| You say... | LLM activates |
|---|---|
| "what should I work on?", "catch me up", session start | `research-session` |
| Mentions a PDF, arXiv URL, "read this paper" | `paper-read` |
| "find papers on X", "lit review", "survey [field]" | `lit-search` |
| "brainstorm", "what if", "should I try X?" | `research-companion` |
| "weekly review", "progress check" | `weekly-review` |
| "sync from vault", "pull notes" | `vault-sync` |
| Multi-angle / parallel review | `orchestrate` |

If you'd rather invoke explicitly, `research-session` also exists as
`.opencode/command/research-session.md`.

## Vault Sync

If you keep a primary Obsidian vault for cross-project knowledge (e.g.,
`~/Documents/OneDrive/obs-notes` with `02 - Projects/<this-project>/`), point
this repo's `vault-sync` at it:

```yaml
# research-state.yaml
vault_sync:
  primary_vault: "~/Documents/OneDrive/obs-notes"
  project_path_in_vault: "02 - Projects/MyProject"
  mirror_target: "docs/.vault-mirror"
```

Then run `bash hooks/vault_sync.sh` (or invoke the `vault-sync` skill in
OpenCode and let the LLM run it). The sync is **one-way** (vault → mirror) with
deletion. Edit notes in the primary vault; the mirror reflects on demand.

## LaTeX Development Workflow

This project uses **native LaTeX** (pdflatex via latexmk).

### Prerequisites

- **TeX Live** installed ([tug.org](https://tug.org/texlive/quickinstall.html))
- **latexmk** (included with TeX Live)
- **zathura** (optional, for PDF viewing)
- **nvim + vimtex** (optional, for editing)

### Local Development

1. **Edit LaTeX files** in `report/`:
   - `main.tex` — document root
   - `preamble.tex` — packages & metadata
   - `sections/*.tex` — chapter/section content
   - `bibliography.bib` — references

2. **Compile and view** using the provided script:

   ```bash
   cd report
   ./compile.sh        # Compile and open in zathura
   ./compile.sh -f     # Force clean rebuild
   ```

3. **In a tmux session** (recommended):

   ```
   tmux new-session -s latex
   tmux split-window -h -l 40   # nvim pane (left, 60% width)
   tmux split-window -v         # latexmk pane (bottom-left)

   # Pane 1 (top-left): nvim report/main.tex
   nvim report/main.tex

   # Pane 2 (bottom-left): latexmk watch
   cd report && latexmk -pdf -pvc main.tex  # Preview continuous mode

   # Pane 3 (right): zathura opens automatically
   ```

4. **Sync with Overleaf** (via GitHub):

   ```bash
   git push origin main
   # Then pull in Overleaf from GitHub
   ```

### Pipeline Compilation

For automated builds (e.g., CI):

```bash
pixi shell
snakemake --cores 4
```

This compiles the LaTeX report as part of the full pipeline.

### References

- [vimtex](https://github.com/lervag/vimtex) — nvim LaTeX plugin with snippets
- [latexmk](https://ctan.org/pkg/latexmk) — Perl script to automate LaTeX compilation
- [zathura](https://pwmt.org/projects/zathura/) — Lightweight PDF viewer

## CI/CD

`.github/workflows/reproduction.yaml` re-runs `snakemake` on every push, PR,
and the 8th of each month. `.github/workflows/lint.yaml` runs ruff + shellcheck
+ yamllint.

## Customising

Each layer is independently editable:

- **Add a skill** → drop a `.opencode/skills/<name>/SKILL.md` and a trigger row in `.opencode/AGENTS.md`.
- **Add a sub-agent** → drop a `.opencode/agent/<name>.md` with frontmatter (`description`, `mode: subagent`, `tools: ...`).
- **Add a Snakemake rule** → write it in `rules/<name>.smk` and `include:` from `Snakefile`.
- **Add documentation** → extend `docs/principles/` with new principle files.

Nothing is hidden behind framework abstractions. If you can read the file, you
can fork it.

## Companions

- **[Snakemake](https://snakemake.readthedocs.io)** — pipeline DAG
- **[Pixi](https://pixi.sh)** — environment and dependency management
- **[TeX Live](https://tug.org/texlive/)** — LaTeX distribution
- **[latexmk](https://ctan.org/pkg/latexmk)** — Perl script to automate LaTeX compilation
- **[vimtex](https://github.com/lervag/vimtex)** — nvim LaTeX plugin
- **[zathura](https://pwmt.org/projects/zathura/)** — Lightweight PDF viewer
- **[Sphinx](https://www.sphinx-doc.org/)** — documentation generator

## Philosophy

Research lives in the handoffs between activities. Reading on Monday, drafting
on Friday, brainstorming in between — without a binding substrate, none of
those activities know the others happened. This template gives you that
substrate as plain text the machine maintains for you.

The hook is non-negotiable: humans abandon knowledge bases because maintaining
cross-references is boring; LLMs don't get bored. Documentation is the system of
record; everything else (state file, event log, primary vault) feeds it.

See the `.opencode/skills/` for detailed workflows and principles in `docs/principles/`.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgements

This template is a synthesis of:

- **`timtroendle/cookiecutter-reproducible-research`** — Snakemake/Conda/Pandoc scaffolding (MIT)
- **`FedericoTartarini/reproducible-research`** — folder-structure conventions (MIT)
- **`andrehuang/researcher-pack`** — skill format, hook design (MIT)
- **Nicholas Carlini** — research-strategy principles (RS1–RS8, derived from his "How to Win a Best Paper Award")
- **Michael Black** — academic-writing principles (B1–F2, distilled from "Writing a Good Scientific Paper")
