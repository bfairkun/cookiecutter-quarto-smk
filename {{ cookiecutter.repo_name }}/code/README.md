# Snakemake workflow: {{cookiecutter.project_name}}

[![Snakemake](https://img.shields.io/badge/snakemake-≥{{cookiecutter.min_snakemake_version}}-brightgreen.svg)](https://snakemake.readthedocs.io)


## Authors

* {{cookiecutter.full_name}} (@{{cookiecutter.username}})

## Usage

### Step 1: Install workflow and dependencies

If you simply want to use this workflow, clone the [latest release](https://github.com/{{cookiecutter.username}}/{{cookiecutter.repo_name}}).

    git clone git@github.com:{{cookiecutter.username}}/{{cookiecutter.repo_name}}.git

If you intend to modify and further develop this workflow, fork this repository. Please consider providing any generally applicable modifications via a pull request.

Install snakemake and the workflow's other dependencies via conda/mamba. If conda/mamba isn't already installed, I recommend [installing miniconda](https://docs.conda.io/en/latest/miniconda.html) and then [install mamba](https://github.com/mamba-org/mamba) in your base environment. Then...

    # move to the snakemake's working directory
    cd {{cookiecutter.repo_name}}/code
    # Create environment for the snakemake
    mamba env create -f envs/{{ cookiecutter.repo_name }}.yaml
    # And activate the enviroment
    conda activate {{ cookiecutter.repo_name }}

### Step 2: Configure workflow

Configure the workflow according to your needs via editing the file `config.yaml`. Cluster settings (and a shared `conda-prefix`) come from the global snakemake profiles in `~/.config/snakemake/` (e.g. `slurm_midway3`); projects don't carry their own.

### Step 3: Execute workflow

Test your configuration by performing a dry-run via

    snakemake -n

Execute the workflow locally via

    snakemake --cores $N

using `$N` cores or run it on the cluster via the global slurm profile.

    snakemake --profile slurm_midway3

See the [Snakemake documentation](https://snakemake.readthedocs.io) for further details.
