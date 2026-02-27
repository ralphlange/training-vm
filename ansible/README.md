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
inside the [`configs/` directory](configs).

### The Main Playbook

*File: `playbook.yml`*

This is the core logic. It defaults the `setup` variable to `local` if not specified.

Each configurable role has a boolean variable (needs to be set `true` to include the role)
and a tag, used to only run specific roles during development.

---

### How to Run

There are multiple ways to control the configuration setup.

#### 1. Default / Soft Link
If you run the playbook without arguments, it looks for `configs/local.yml`.
You can use a symlink to point `local.yml` to your desired config.

```bash
# Link local to my_config
cd configs
ln -sf my_config.yml local.yml
cd ..

# Run
ansible-playbook playbook.yml
```
*Result: Will override role defaults with settings from my_config.*

#### 2. Command Line Selection
You can ignore the default/symlink and strictly specify
which file to load using the extra vars flag (`-e`).

```bash
# Run with foobar config
ansible-playbook playbook.yml -e "setup=foobar"
```
*Result: Will override role defaults with settings from foobar.*

#### 3. Fallback to Role Defaults
If you point to a config file that is empty,
Ansible will use the variables defined in `roles/*/defaults/main.yml`.

To see the **Role Defaults** in action
(assuming you just want to see the base behavior),
create a minimal default:

*File: `configs/base.yml`* (Empty file)
```bash
touch configs/base.yml
ansible-playbook playbook.yml -e "setup=base"
```
*Result: Will use the default values defined in the roles.*

#### 4. Command Line Override of Specific Variables
You can always set specific variables on the command line,
which will override any values in role defaults or setup files.

```bash
# Run with foobar config, but set in_container flag
ansible-playbook playbook.yml -e "setup=foobar" -e "in_container=true"
```
*Result: Will override role defaults with settings from foobar and set in_container.*

### Variable Precedence
In this setup, the variable precedence (priority) is:
1.  **Command line (`-e`)**: Highest (overrides everything).
2.  **Selected setup (using playbook `vars_files`)**: Middle (overrides defaults).
3.  **Role Defaults**: Lowest (used only if not defined elsewhere).
