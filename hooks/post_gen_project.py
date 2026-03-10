#!/usr/bin/env python

"""
Post cookiecutter hook script to generate a conda environment for snakemake and initialize git repos with submodules
"""

import sys
import os
import subprocess
import collections
import shutil
from collections import OrderedDict


def indent_lines(text, indent='\t'):
    return ''.join(f"{indent}{line}" if line.strip() else line for line in text.splitlines(keepends=True))

def FindCondaExecutable():
    """
    Return either 'mamba', 'conda', or None depending on which executables are available.
    """
    if shutil.which('mamba'):
        return 'mamba'
    elif shutil.which('conda'):
        return 'conda'
    else:
        return None

# Load the context from cookiecutter.json
submodules = eval("{{ cookiecutter.submodules }}", {"OrderedDict": collections.OrderedDict})

# Initialize a git repository in the project directory
subprocess.run(["git", "init"], check=True)

# Add each submodule, supporting extra arguments like branch
for submodule_name, submodule_info in submodules.items():
    if isinstance(submodule_info, dict):
        remote_url = submodule_info.get("url")
        branch = submodule_info.get("branch")
    else:
        remote_url = submodule_info
        branch = None
    submodule_dest = "code/module_workflows/" + submodule_name
    cmd = ["git", "submodule", "add"]
    if branch:
        cmd += ["-b", branch]
    cmd += [remote_url, submodule_dest]
    subprocess.run(cmd, check=True)

# Update the submodules
subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)

print("Git repository initialized and submodules (if provided) added successfully.")


# Make conda env
make_conda_env = '{{ cookiecutter.make_conda_env }}'
if make_conda_env == 'y':
    conda_executable = FindCondaExecutable()
    if not conda_executable:
        print('ERROR: could not find conda executable' % make_conda_env)
        sys.exit(1)
    print("Attempting to create conda environment from code/envs/{{ cookiecutter.repo_name }}.yaml")
    sys.exit(
            os.system("%s env create -f code/envs/{{ cookiecutter.repo_name }}.yaml" %conda_executable)
            )
elif make_conda_env =='n':
    pass
else:
    print('ERROR: %s is not a valid option for make_conda_env' % make_conda_env)
    # exits with status 1 to indicate failure
    sys.exit(1)


# Generate Snakefile module blocks
snakefile_path = os.path.join('code', 'Snakefile')
with open(snakefile_path, 'r') as f:
    snakefile_content = f.read()

module_blocks = []
for submodule_name in submodules:
    module_blocks.append(f"""\
module {submodule_name}:
    snakefile: "module_workflows/{submodule_name}/Snakefile"
    prefix: "{submodule_name}"
    config: config["{submodule_name}"]
use rule * from {submodule_name} as {submodule_name}_*
# some rules in the module are shell commands which call a script assuming the workdir is the other workdir. use symlinks for scripts to fix.
CreateSymlinksOfDir1ContentsIntoDir2("module_workflows/{submodule_name}/scripts/", "scripts/")
""")

snakefile_content = snakefile_content.replace(
    '# SUBMODULE_BLOCKS_PLACEHOLDER',
    '\n'.join(module_blocks)
)
with open(snakefile_path, 'w') as f:
    f.write(snakefile_content)

# Generate config.yaml submodule sections
config_path = os.path.join('code', 'config', 'config.yaml')
with open(config_path, 'r') as f:
    config_content = f.read()

config_blocks = []
for submodule_name in submodules:
    sub_cfg_path = os.path.join('code', 'module_workflows', submodule_name, 'config', 'config.yaml')
    sub_cfg_content = ''
    if os.path.exists(sub_cfg_path):
        with open(sub_cfg_path, 'r') as sub_cfg:
            sub_cfg_content = indent_lines(sub_cfg.read(), indent='    ')
    config_blocks.append(f"""\
{submodule_name}:
    ## Define {submodule_name} specific-config values that will overwrite workflow-wide config values if they are defined above
    ## If the {submodule_name} requires config values (eg from a config.yaml), must copy paste those values here if not already defined above
{sub_cfg_content}""")

config_content = config_content.replace(
    '# SUBMODULE_CONFIG_PLACEHOLDER',
    '\n'.join(config_blocks)
)
with open(config_path, 'w') as f:
    f.write(config_content)
