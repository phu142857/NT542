# Auto-VM: KVM Virtual Machine Provisioning with Ansible

A complete project for provisioning KVM virtual machines using Ansible and cloud-init.

## Project Structure

```
auto-vm/
- ansible/
  - inventory/hosts.ini
  - group_vars/all.yml
  - roles/vm_create/tasks/main.yml
  - roles/vm_create/templates/cloud-init/user-data.j2
  - roles/vm_create/templates/cloud-init/meta-data.j2
  - playbooks/create-vm.yml
- images/base/
- images/disks/
- cloud-init/seed-iso/
- scripts/gen-seed.sh
- scripts/cleanup.sh
- vars/vm-list.yml
- README.md
```

## Prerequisites

1. **KVM/QEMU installed**:
   ```bash
   # Ubuntu/Debian
   sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst
   
   # Start libvirt service
   sudo systemctl enable libvirtd
   sudo systemctl start libvirtd
   
   # Add user to libvirt group
   sudo usermod -aG libvirt $USER
   # Logout and login again
   ```

2. **Ansible installed**:
   ```bash
   sudo apt install ansible
   ```

3. **Cloud-init tools**:
   ```bash
   sudo apt install cloud-image-utils genisoimage
   ```

4. **Base images** (place in `images/base/`):
   - `ubuntu-22.04.qcow2` - Ubuntu 22.04 cloud image
   - `ubuntu-24.04.qcow2` - Ubuntu 24.04 cloud image
   
   Download from: https://cloud-images.ubuntu.com/

## VM Configuration

The project provisions 2 VMs:

- **u22** (Ubuntu 22.04)
  - User: `s1`
  - Password: `Phuqwaszx142@`
  - RAM: 2GB
  - CPU: 2 cores
  - Disk: 20GB

- **u24** (Ubuntu 24.04)
  - User: `s2`
  - Password: `Phuqwaszx142@`
  - RAM: 2GB
  - CPU: 2 cores
  - Disk: 20GB

## Usage

### 1. Prepare Base Images

Download Ubuntu cloud images and place them in `images/base/`:

```bash
# Create directories
mkdir -p images/base

# Download Ubuntu 22.04 cloud image
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img -O images/base/ubuntu-22.04.qcow2

# Download Ubuntu 24.04 cloud image
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img -O images/base/ubuntu-24.04.qcow2
```

### 2. Make Scripts Executable

```bash
chmod +x scripts/gen-seed.sh
chmod +x scripts/cleanup.sh
```

### 3. Run the Playbook

```bash
cd auto-vm
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/create-vm.yml
```

The playbook will:
- Create qcow2 disks using backing files
- Generate cloud-init configurations
- Create seed ISOs
- Provision VMs with virt-install
- Display VM IP addresses
- **Automatically add VM IPs to cis-ubuntu inventory**

### 4. SSH into VMs

After the playbook completes, you can SSH into the VMs:

```bash
# SSH to u22 VM
ssh s1@<u22-ip-address>

# SSH to u24 VM  
ssh s2@<u24-ip-address>
```

**Note**: Use the password `Phuqwaszx142@` or SSH keys if configured.

### 5. Get VM IP Addresses

To get the IP addresses of running VMs:

```bash
# Get IP of u22
virsh domifaddr u22

# Get IP of u24
virsh domifaddr u24

# Or get all VM IPs
for vm in u22 u24; do
    echo "=== $vm ==="
    virsh domifaddr $vm
    echo
done
```

### 6. Cleanup VMs

To remove a VM and all its resources:

```bash
# Remove u22 VM
./scripts/cleanup.sh u22

# Remove u24 VM
./scripts/cleanup.sh u24
```

## SSH Key Configuration

The project automatically injects your SSH public key (`~/.ssh/id_rsa.pub`) into the VMs. If you want to use a different key:

1. Edit `ansible/group_vars/all.yml`
2. Change the `ssh_public_key` value

## Automatic Inventory Integration

The playbook automatically adds newly created VMs to the cis-ubuntu inventory file:

- **Target file**: `../cis-ubuntu/inventory/hosts.ini`
- **Format**: `<IP> ansible_user=<username> ansible_ssh_private_key_file=../NT542`
- **Duplicate prevention**: Checks if IP already exists before adding
- **Real-time updates**: IPs are added as soon as VMs get network connectivity

### Manual Inventory Management

If you need to manually manage the inventory:

```bash
# View current inventory
cat ../cis-ubuntu/inventory/hosts.ini

# Remove a VM from inventory
sed -i '/<IP>/d' ../cis-ubuntu/inventory/hosts.ini

# Test Ansible connectivity
cd ../cis-ubuntu
ansible -i inventory/hosts.ini all -m ping
```

## Customization

### Adding New VMs

Edit `vars/vm-list.yml` to add new VMs:

```yaml
vms:
  - name: u20
    user: s3
    memory: 4096
    vcpus: 4
    disk_size: 50
    state: present
```

### Modifying VM Configuration

Edit `ansible/group_vars/all.yml` to change default settings:

- `vm_memory_mb`: Default RAM in MB
- `vm_vcpus`: Default CPU cores
- `vm_disk_size_gb`: Default disk size in GB
- `vm_network`: Network type (default: "default")

### Cloud-init Customization

Edit the cloud-init templates in `ansible/roles/vm_create/templates/cloud-init/`:

- `user-data.j2`: User configuration, packages, SSH settings
- `meta-data.j2`: Instance metadata

## Troubleshooting

### VM Not Getting IP

1. Check if the default network is active:
   ```bash
   virsh net-list --all
   virsh net-start default
   virsh net-autostart default
   ```

2. Check VM console:
   ```bash
   virsh console <vm-name>
   ```

### Permission Issues

Ensure your user is in the `libvirt` group:
```bash
groups $USER
sudo usermod -aG libvirt $USER
# Logout and login again
```

### Cloud-init Not Working

1. Check cloud-init logs in the VM:
   ```bash
   ssh <user>@<vm-ip>
   sudo cat /var/log/cloud-init.log
   ```

2. Verify seed ISO was created correctly:
   ```bash
   ls -la cloud-init/seed-iso/
   ```

## Security Notes

- The password `Phuqwaszx142@` is hardcoded for demonstration
- In production, use SSH keys and disable password authentication
- Consider using Ansible Vault for sensitive data

## Support

For issues with:
- **KVM/libvirt**: Check `journalctl -u libvirtd`
- **Ansible**: Run with `-vvv` for verbose output
- **Cloud-init**: Check VM logs as shown above