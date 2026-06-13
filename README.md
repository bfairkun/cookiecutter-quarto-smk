# cookiecutter-quarto-smk

Cookiecutter template for Snakemake workflows and [Quarto](https://quarto.org/) documentation.  
This project template is inspired by the [cookiecutter snakemake project template](https://github.com/snakemake-workflows/cookiecutter-snakemake-workflow) and the suggested project structure for [workflowr](https://jdblischak.github.io/workflowr/articles/wflow-01-getting-started.html).  
This template now uses Quarto for documentation and static site generation, supporting `.qmd`, `.Rmd`, and `.ipynb` notebooks.

---

### USAGE

Install cookiecutter:

```
pip install cookiecutter
```

Start creating a snakemake-workflow from cookiecutter:
```
cookiecutter https://github.com/bfairkun/cookiecutter-quarto-smk.git
```

After filling the prompts, this will create a project template with the following directory structure:

```
{{ cookiecutter.repo_name }}/
├── AGENTS.md                 # Project conventions for AI coding agents (cross-vendor)
├── CLAUDE.md                 # One-liner: @AGENTS.md — Claude Code follows the reference
├── analysis
│   ├── about.qmd
│   ├── index.qmd
│   ├── license.qmd
│   ├── _quarto.yml
│   └── scripts              # Ad-hoc notebook helper scripts (not in Snakemake)
├── code
│   ├── config
│   │   ├── config.yaml
│   │   └── samples.tsv
│   ├── envs
│   │   ├── {{ cookiecutter.repo_name }}.yaml
│   │   ├── jupyter.yml
│   │   ├── myenv.yaml
│   │   └── r_essentials.yml
│   ├── module_workflows
│   ├── README.md
│   ├── rules
│   │   ├── common.smk
│   │   └── other.smk
│   ├── scripts
│   │   └── common
│   │       └── __init__.py
│   ├── Snakefile
│   └── snakemake_profiles
│       └── slurm
│           ├── cluster-config.yaml
│           ├── config.yaml
│           ├── slurm-jobscript.sh
│           ├── slurm-status.py
│           ├── slurm-submit.py
│           └── slurm_utils.py
├── {{ cookiecutter.repo_name }}.Rproj
├── data
│   └── README.md
├── docs
│   └── assets
├── output
│   └── README.md
├── README.md
```

---

### Guidelines for project organization

- Optionally track the entire project with `git init` in the newly created project root.
- Use the `code` directory to create a reproducible Snakemake pipeline which does heavy-lifting analysis to be run on a cluster environment from `code` as the working directory. The `code/.gitignore` makes it easy to git track all the code, but ignore tracking the potentially large files in the `code` directory. As you write the Snakemake pipeline, it is ok to create large untracked files which are too big to push to GitHub. Use Snakemake to do heavy lifting (e.g., download NGS data, align, etc.) and process the data to small files that can be easily tracked and pushed to GitHub. The cookiecutter will optionally create a conda environment for Snakemake with some basic NGS processing software in `code/envs/{{ cookiecutter.repo_name }}.yaml`. If you need to create additional rule-specific conda environments for Snakemake, they should also be saved in `code/envs/`. Using [snakemake modules](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#modules) is a nice way to start a workflow, as in [this example](https://github.com/bfairkun/sm_splicingmodulators/blob/265a0f233c26c10c75e5ca923d94400daa7e40b3/code/Snakefile#L8-L19) where I can include the code for a submodule as a nested git submodule. See the `code/README.md` for more on my Snakemake project template.
- Write the Snakemake pipeline to output smaller processed files (e.g., gene x sample count tables for RNA-seq) to `output` where they will be tracked by git.
- Raw data (that should never be directly edited) that is small enough to track with git should go in `data`.
- Use the `analysis` directory to write Quarto (`.qmd`), Rmarkdown (`.Rmd`), and Jupyter notebook (`.ipynb`) files to document your thoughts and analysis of processed data. If these notebook files only read in the data files tracked in `output` or `data`, it should be easy for anyone to edit or re-run your notebooks by cloning this repo (without needing to run Snakemake or do the computationally intensive things).
    - To render notebooks into a static site and host on GitHub, use Quarto to render `.qmd`, `.Rmd`, and `.ipynb` files into HTML and place them into `docs`. The `docs/assets` directory can be used to save images that can also be referenced in notebooks and their rendered HTMLs. To enable GitHub Pages hosting, add the project to GitHub and modify the project settings to build a site from the `/docs` folder (in the "Pages" section of project settings).
    - Occasionally, you may write notebooks that need access to large untracked files output by Snakemake. In this case, it is helpful to follow a naming convention to specify which notebooks need access to these large files, so it is clear what notebooks can be run simply by cloning the repo, versus needing access to large untracked files.
- **Ad-hoc notebook helper scripts** (one-off data-prep that does not belong in the Snakemake pipeline — e.g. a per-barcode pileup that only a specific notebook depends on) go in `analysis/scripts/`, named after the notebook they pair with (e.g. `analysis/scripts/20260514_variant_exploration_pileup_per_barcode.py`). The script docstring should state which notebook it pairs with and include the exact CLI used. The notebook should reference the script by path and show the command that produced the input files. Outputs of these scripts go to `code/scratch/` (regeneratable) or `output/` (committed). If a helper later turns out to be reusable, promote it to `code/scripts/` and wire it into a `code/rules/*.smk` rule.

---

### Conventions for AI coding agents

Every project scaffolded by this template includes an `AGENTS.md` at the project root that documents project conventions for AI coding agents (Claude Code, OpenAI Codex CLI, Aider, etc.). `AGENTS.md` is a cross-vendor convention now read by most agent tooling; the template also ships a `CLAUDE.md` whose contents are just `@AGENTS.md` so Claude Code follows the same file. Edit `AGENTS.md` in a project to override or extend the defaults for that project.

---

### Quarto Usage

- The `analysis/_quarto.yml` file configures the Quarto site.
- The `analysis/index.qmd` file lists all notebooks in the `analysis/` directory.
- To render the site, run the following in the `analysis/` directory:

    ```
    quarto render
    ```

- The rendered HTML will appear in the `docs/` directory, ready for GitHub Pages.

---

Start scripting and documenting your project!
