## Available User-Level Roles

### archiver-appliance

Installs a minimal setup of the EPICS Archiver Appliance.
(Single tomcat, single engine.)

Don't expect great performance - this is for training purposes:
a few PVs at low rates over a short time.

### bluesky

Installs the containerized bluesky ecosystem
for the training session by Marcel Bajdel and Luca Porzio (HZB).

### catrust

Installs an institutional CA certificate to be used
behind a deep packet inspection corporate firewall.

### docker

Installs the docker ecosystem (podman on RedHat derivates).

*Must run before the first reboot to use rootful containers.*

### epics-modules

Generic role to build and install a list of standard (C/C++) EPICS modules.

Used to install EPICS Base, ASYN, areaDetector, SNC/Sequencer, OPC UA, etc...

### epics-tools

Installs the Phoebus GUI framework.

### oac-tree

Installs the oac-tree behavior-tree-based operational sequencer.


## Internal Roles

### common

Is always run, mandatory, to set global things.

### initial_setup

Is run once when the VM is created, to update and install the base system
including the necessary tooling like git, Ansible, etc.

### java

Installs the OpenJDK Java environment.

