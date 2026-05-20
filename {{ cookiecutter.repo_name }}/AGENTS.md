# AGENTS.md — Project conventions for AI coding agents

This file documents the layout and working conventions for this project so that any AI coding agent (Claude Code, OpenAI Codex CLI, Aider, etc.) can pick up the right habits automatically. Human contributors should also follow these conventions; see `README.md` for the human-oriented project overview.

If you are an agent: read this file before making structural decisions (where to put a new file, how to document a notebook helper, where to write output). Conventions here override generic defaults.

---

## Project layout

```
{{ cookiecutter.repo_name }}/
├── analysis/        # Quarto/Rmarkdown notebooks (.qmd, .Rmd, .ipynb) + ad-hoc helpers
│   └── scripts/     # One-off notebook helper scripts (NOT in Snakemake)
├── code/            # Snakemake pipeline and production scripts
│   ├── rules/       # *.smk files
│   ├── scripts/     # Production scripts called by Snakemake rules
│   ├── envs/        # Conda env YAMLs
│   ├── config/
│   ├── module_workflows/  # Git submodules for shared Snakemake modules
│   ├── scratch/     # Regeneratable intermediates — DO NOT commit large files
│   └── Snakefile
├── data/            # Small, never-edited raw data (git-tracked)
├── output/          # Pipeline outputs intended to be committed and shared
└── docs/            # Rendered Quarto HTML site (GitHub Pages)
```

## Where things go

| File type | Location | Notes |
|---|---|---|
| Snakemake-invoked script | `code/scripts/` | Any script a `rules/*.smk` file calls. Production code. |
| Notebook helper (one-off, not in Snakemake) | `analysis/scripts/` | Named after the notebook it pairs with, e.g. `20260514_variant_exploration_pileup_per_barcode.py`. Docstring states the pairing + exact CLI. |
| Snakemake rule | `code/rules/<topic>.smk` | Grouped by topic, not by date. |
| Conda env YAML | `code/envs/<name>.yaml` | Don't modify `py_general`; create `claude_<DescriptiveName>` if you need a new env. |
| Quarto notebook | `analysis/YYYYMMDD_<topic>.qmd` | Date-prefixed; one notebook per analysis question. |
| Rendered notebook HTML | `docs/` | Output of `quarto render`; tracked in git for GitHub Pages. |
| Pipeline intermediate (large, regeneratable) | `code/scratch/` | Not committed; safe to delete and rebuild. |
| Pipeline output (small, shareable) | `output/` | Committed; the "answer" of the pipeline. |
| Raw data | `data/` | Small, never edited. |

## Convention: ad-hoc notebook helper scripts

Sometimes a notebook needs a one-off data-prep step that doesn't belong in the Snakemake pipeline — e.g. a per-barcode pileup that only one notebook depends on. These go in `analysis/scripts/`.

Rules:

1. **Name** the script after the notebook it pairs with: `<notebook_stem>_<purpose>.py`.
2. The script's **docstring** must state which notebook it pairs with and include the exact CLI used to generate its outputs.
3. The notebook must **reference the script by path** and show the exact command that produced the input files it loads. Use a Quarto callout or markdown block, e.g.:

   > This analysis depends on `analysis/scripts/<notebook_stem>_<purpose>.py`, which was run once to produce `code/scratch/<output>.tsv`:
   >
   > ```bash
   > python analysis/scripts/<notebook_stem>_<purpose>.py <args>
   > ```

4. **Outputs** of these scripts go to `code/scratch/` (regeneratable) or `output/` (shareable). Not in `analysis/`.
5. If a helper later turns out to be reused across notebooks or worth pipelining, **promote** it: move to `code/scripts/`, wire a rule into `code/rules/<topic>.smk`, and update the notebook to read from the rule's output path instead of running the script directly.

## Quarto notebooks

- The `analysis/_quarto.yml` configures the site; `analysis/index.qmd` lists notebooks.
- Render with `quarto render` from `analysis/`. The HTML lands in `../docs/`.
- For self-contained HTML (e.g. for sharing without the assets), add `--embed-resources` or set `embed-resources: true` in the notebook YAML.
- Prefer adding `code-fold: true` to the notebook YAML so the rendered HTML is readable without code clutter.
- If a notebook depends on large files outside the repo (e.g. raw BAMs on the cluster), say so explicitly in the notebook prose so a fresh `git clone` reader knows what they can vs cannot run.

## Snakemake

- Work from `code/` as the working directory when invoking Snakemake.
- Use rule-specific conda envs in `code/envs/` rather than a monolithic env.
- Pipeline outputs that other notebooks or downstream stages read should land in `output/` (small, committed) or `code/scratch/` (large, regeneratable).
- Snakemake submodules go in `code/module_workflows/` as git submodules (one per workflow).

## What NOT to do

- Don't write production helpers into `code/scratch/` — that directory is for regeneratable junk.
- Don't write large files into `output/` — keep `output/` small and committed.
- Don't bypass the cookiecutter convention by inventing a new top-level directory.
- Don't modify the shared `py_general` conda env. Make a new `claude_*` env if you need additional packages.

## For Claude Code specifically

The repo also contains a `CLAUDE.md` that simply references this file (`@AGENTS.md`). Claude Code follows that reference. User-level CLAUDE.md additions live in `~/.claude/CLAUDE.md`.
