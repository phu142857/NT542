# CIS Ubuntu Automation - Quick Start Guide

This guide explains how to set up SSH access and run Ansible automation on multiple Ubuntu servers.

---

## 1. Generate SSH Key

On the control machine (server1), generate a new SSH key:

```bash
ssh-keygen -f ~/NT542
```

---

## 2. Copy SSH Key to Target Servers

Copy the public key to each target server:

```bash
ssh-copy-id -i ~/NT542.pub server2@192.168.122.174
ssh-copy-id -i ~/NT542.pub server3@192.168.122.112
```

---

## 3. Start SSH Agent and Add Key

Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

Add the private key:

```bash
ssh-add ~/NT542
```

---

## 4. Configure Ansible Inventory

Edit the inventory file:

```bash
nano inventory/hosts.ini
```

Add the following:

```ini
[servers]
192.168.122.174 ansible_user=server2 ansible_ssh_private_key_file=~/NT542
192.168.122.112 ansible_user=server3 ansible_ssh_private_key_file=~/NT542
```

---

## 5. Test SSH Connection

Verify that Ansible can connect to all servers:

```bash
ansible all -m ping
```

Expected output:

```
SUCCESS => "pong"
```

---

## 6. Run Ansible Playbook

Execute the automation:

```bash
ansible-playbook playbooks/site.yml
```

---

## 7. (Optional) Run Compliance Scan

Run audit playbook:

```bash
ansible-playbook playbooks/audit.yml
```

---

## Notes

* Make sure all target servers are reachable via SSH
* Ensure Python is installed on target machines
* Run commands from the project root directory

---

## Architecture Overview

```
Control Node (server1)
        │
        │ SSH (key-based)
        ▼
Server2 -------- Server3
```

---

