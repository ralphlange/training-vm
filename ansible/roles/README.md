# Available roles

## EPICS Modules

### m-areadetector
The AreaDetector image processing framework
(modules Core, SimDetector and PVADriver)
and their dependencies Busy, SScan and Calc.

### m-base
EPICS Base C++ and PVXS.

### m-opcua
OPC UA Device Support and the open62541 low-level driver.

### m-p4p
Python wrapper for PVAccess (PVXS-based) and PVA Gateway.

### m-pvaPy
Python wrapper for PVAccess (based on the classical PVA stack).

### m-seq
State Notation language compiler and Sequencer.

### m-stream
StreamDevice Device Support.

## Phoebus and Services

### epics-tools
Control System Studio / Phoebus.

### archiver-appliance
Minimal install of the EPICS Archiver Appliance.

## Other Clients

### oac-tree
High-level sequencer for automation, operation and control.

## Bluesky Modules

### bluesky
Containerized training setup of Bluesky.

## System Level Roles

### catrust
Enterprise CA certificate install
(needed behind deep packet inspection firewalls).

## Internal Modules
Low-level stuff and dependencies of the above.

### m-asyn
The ASYN Driver framework.

### m-autosave
The AutoSaveRestore (EPICS Process Database persistence) module.

### common
Common tasks. (mandatory)

### docker
Installation of Docker or Podman to run containers.

### epics-module
Generic task called by the m-* roles to install EPICS C/C++ modules.

### initial_setup
One-off role called at the first run in a freshly provisioned VM.

### java
Java SDK needed for Phoebus and Services.
