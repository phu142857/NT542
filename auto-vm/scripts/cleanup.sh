#!/bin/bash

# Cleanup VM resources
# Usage: cleanup.sh <vm-name>

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <vm-name>"
    echo "Example: $0 u22"
    exit 1
fi

VM_NAME="$1"
VM_BASE_PATH="/home/teifu142/ATE/UIT/NT542/auto-vm"
DISK_PATH="${VM_BASE_PATH}/images/disks/${VM_NAME}.qcow2"
ISO_PATH="${VM_BASE_PATH}/cloud-init/seed-iso/${VM_NAME}.iso"
USER_DATA="${VM_BASE_PATH}/cloud-init/seed-iso/${VM_NAME}-user-data"
META_DATA="${VM_BASE_PATH}/cloud-init/seed-iso/${VM_NAME}-meta-data"

echo "Cleaning up VM: $VM_NAME"

# Stop and undefine VM if it exists
if virsh dominfo "$VM_NAME" >/dev/null 2>&1; then
    echo "Stopping VM: $VM_NAME"
    virsh destroy "$VM_NAME" 2>/dev/null || true
    
    echo "Undefining VM: $VM_NAME"
    virsh undefine "$VM_NAME" --remove-all-storage --nvram || true
fi

# Remove disk file
if [ -f "$DISK_PATH" ]; then
    echo "Removing disk: $DISK_PATH"
    rm -f "$DISK_PATH"
fi

# Remove ISO file
if [ -f "$ISO_PATH" ]; then
    echo "Removing ISO: $ISO_PATH"
    rm -f "$ISO_PATH"
fi

# Remove cloud-init files
if [ -f "$USER_DATA" ]; then
    echo "Removing user-data: $USER_DATA"
    rm -f "$USER_DATA"
fi

if [ -f "$META_DATA" ]; then
    echo "Removing meta-data: $META_DATA"
    rm -f "$META_DATA"
fi

echo "Cleanup completed for VM: $VM_NAME"