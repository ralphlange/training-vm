# epics-modules role (Legacy Wrapper)

This role has been refactored to use a new modular structure. It now acts as a wrapper that calls several high-level roles based on the `epics_modules_list` variable.

## New Structure

The refactored system consists of:
- `epics-module`: An internal generic role used to install one or more EPICS modules.
- High-level roles:
    - `m-base`: Installs EPICS Base and PVXS.
    - `m-p4p`: Installs P4P (depends on `m-base`).
    - `m-pvaPy`: Installs pvaPy (depends on `m-base`).
    - `m-seq`: Installs SNCSEQ (depends on `m-base`).
    - `m-asyn`: Installs ASYN (depends on `m-base` and `m-seq`).
    - `m-autosave`: Installs autosave (depends on `m-base`).
    - `m-areadetector`: Installs busy, sscan, calc, ADCore, ADSimDetector, and ADPVADriver (depends on `m-autosave` and `m-pvaPy`).
    - `m-opcua`: Installs OPC UA (depends on `m-base`).

## Usage

You can still use this role with `epics_modules_list` for backward compatibility. However, it is recommended to use the high-level roles directly in your playbooks for better control over dependencies and modularity.

### Old usage (still supported):
```yaml
- role: epics-modules
  vars:
    epics_modules_list:
      - base
      - asyn
```

### Recommended new usage:
```yaml
- role: m-asyn
```
(This will automatically include `m-base` and `m-seq` as dependencies).
