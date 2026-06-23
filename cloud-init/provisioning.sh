#!/bin/bash
# provisioning.sh - One-off initialization script for cloud-init

set -xe

# These variables can be seeded via cloud-init environment or defaults
TRAINING_VM_REPO="${TRAINING_VM_REPO:-https://github.com/epics-training/training-vm.git}"
TRAINING_VM_BRANCH="${TRAINING_VM_BRANCH:-main}"
ANSIBLE_ARGS="${ANSIBLE_ARGS:-}"
INSTALL_GRAPHICS="${INSTALL_GRAPHICS:-false}"

# Determine installer
if command -v apt-get >/dev/null; then
    installer="apt"
elif command -v dnf >/dev/null; then
    installer="dnf"
else
    echo "Unknown installer"
    exit 1
fi

# Install Ansible and Git
if [[ "$installer" == "apt" ]]; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y git ansible python3-jmespath
elif [[ "$installer" == "dnf" ]]; then
    dnf install -y epel-release || dnf update -y --refresh
    dnf install -y git ansible python3-jmespath
fi

# Clone the training-vm repo
mkdir -p /opt/epics-setup
git clone -b "$TRAINING_VM_BRANCH" "$TRAINING_VM_REPO" /opt/epics-setup/training-vm

cd /opt/epics-setup/training-vm/ansible

# Install dependencies
ansible-galaxy install -r requirements.yml || true

# Run the playbook
# We pass install_graphics and initial_setup=true
ansible-playbook playbook.yml \
    -e "initial_setup=true" \
    -e "install_graphics=$INSTALL_GRAPHICS" \
    $ANSIBLE_ARGS

# Signal completion and shutdown
# We use a flag file that the host can poll for if needed, or just shutdown.
echo "Provisioning complete" > /var/log/provisioning_complete
poweroff
