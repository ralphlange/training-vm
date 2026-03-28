## Training-VM Ansible Setup

### Overview

1.  **Local Execution:**
    Ansible always targets `localhost` with a `local` connection.
    `inventory` is a simple minimal file defining localhost.
2.  **Configuration Defaults:**
    Default configuration settings are defined in the role scope in `roles/x/defaults/main.yml`.
    (This has the lowest priority and is easily overridden.)
3.  **Dynamic Configuration:**
    The `vars_files` directive in the playbook
    combined with a variable (`setup`)
    is used to dynamically load specific settings files.
4.  **Containerized CI Builds:**
    On GitHub Actions, the Ansible install is tested inside containers,
    which are created as part of the pipeline for all four flavours.

### Run-Specific Setup Files

Setups for different runs are held in configuration profiles
inside the [`vars/` directory](configs).

### The Main Playbook

*File: `playbook.yml`*

This is the core logic.

Each configurable role has a boolean variable (needs to be set `true` to include the role)
and a tag, used to only run specific roles during development.

---

### How to Run

There are multiple ways to control the configuration setup.

#### 1. Command Line Selection
Specify settings files to load
using the extra vars flag (`-e`).

```bash
# Run with foobar.yml config
ansible-playbook playbook.yml -e "@vars/foobar.yml"
```
*Result: Will override role defaults with settings from foobar.yml*

#### 2. Fallback to Role Defaults
If you do not specify a config file,
Ansible will use the variables defined in `roles/*/defaults/main.yml`.

#### 3. Command Line Override of Specific Variables
You can always set specific variables on the command line,
which will override any values in role defaults or setup files.

```bash
# Run with foobar config, but set in_container flag
ansible-playbook playbook.yml -e "vars/@foobar.yml" -e "in_container=true"
```
*Result: Will override role defaults with settings from foobar.yml
and set in_container to true.*

### Variable Precedence
In this setup, the variable precedence (priority) is:
1.  **Command line (`-e`)**: Highest (overrides everything).
2.  **Selected setup (using setup files in `vars`)**: Middle (overrides defaults).
3.  **Role Defaults**: Lowest (used only if not defined elsewhere).
