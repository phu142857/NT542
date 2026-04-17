#!/bin/bash

# Generate cloud-init seed ISO
# Usage: gen-seed.sh <path-to-cloud-init-files-without-extension>

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <path-to-cloud-init-files-without-extension>"
    echo "Example: $0 /path/to/seed-iso/u22"
    exit 1
fi

SEED_PATH="$1"
USER_DATA="${SEED_PATH}-user-data"
META_DATA="${SEED_PATH}-meta-data"
ISO_FILE="${SEED_PATH}.iso"

if [ ! -f "$USER_DATA" ]; then
    echo "Error: User data file not found: $USER_DATA"
    exit 1
fi

if [ ! -f "$META_DATA" ]; then
    echo "Error: Meta data file not found: $META_DATA"
    exit 1
fi

echo "Generating cloud-init seed ISO: $ISO_FILE"

# Try cloud-localds first (preferred method)
if command -v cloud-localds >/dev/null 2>&1; then
    cloud-localds "$ISO_FILE" "$USER_DATA" "$META_DATA"
else
    # Fallback to genisoimage
    if command -v genisoimage >/dev/null 2>&1; then
        genisoimage -output "$ISO_FILE" -volid cidata -joliet -rock "$USER_DATA" "$META_DATA"
    else
        echo "Error: Neither cloud-localds nor genisoimage found. Please install one of them."
        echo "  Ubuntu/Debian: sudo apt install cloud-image-utils genisoimage"
        echo "  CentOS/RHEL: sudo yum install genisoimage"
        exit 1
    fi
fi

echo "Seed ISO generated successfully: $ISO_FILE"