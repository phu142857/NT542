# NT542 - CIS Ubuntu Security Hardening Project

A comprehensive security hardening project for Ubuntu 24.04 LTS systems implementing the CIS Benchmark v1.0.0 with automated virtual machine creation, security hardening, and compliance reporting.

## Project Overview

NT542 provides a complete security hardening solution with three main components:

- **auto-vm**: Automated virtual machine creation and management
- **cis-ubuntu**: CIS Ubuntu Linux 24.04 LTS Benchmark implementation
- **NT542-report**: Security assessment and compliance reporting

## Architecture

```
NT542 Project
    |
    |-- auto-vm/           # VM automation
    |-- cis-ubuntu/        # Security hardening
    |-- NT542-report/      # Compliance reports
    |-- README.md          # This file
```

## Quick Start Guide

### Prerequisites
- Ansible 2.9+ installed
- Virtualization support (for auto-vm)
- Ubuntu 24.04 LTS target systems

### 1. Environment Setup

Generate SSH key for automation:
```bash
ssh-keygen -f ~/NT542
eval "$(ssh-agent -s)"
ssh-add ~/NT542
```

### 2. Virtual Machine Creation (Optional)

If you need to create test VMs:
```bash
cd auto-vm
ansible-playbook playbooks/create-vm.yml --ask-become-pass
```

### 3. Security Hardening

Configure target systems:
```bash
cd cis-ubuntu
nano inventory/hosts.ini  # Add your target servers
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml --ask-become-pass
```

### 4. Security Assessment

Run compliance scans:
```bash
cd cis-ubuntu
ansible-playbook -i inventory/hosts.ini playbooks/run_security_assessment.yml --ask-become-pass
```

### 5. View Reports

Check compliance reports:
```bash
cd NT542-report
# View HTML reports in results/ directory
```

## Component Details

### auto-vm - Virtual Machine Automation

Automated creation and configuration of Ubuntu virtual machines for testing and development.

**Features:**
- Automated VM provisioning
- Network configuration
- SSH key setup
- Cloud-init integration

**Usage:**
```bash
cd auto-vm
ansible-playbook playbooks/create-vm.yml
```

### cis-ubuntu - Security Hardening

Complete implementation of CIS Ubuntu Linux 24.04 LTS Benchmark with 7 security phases.

**Phases:**
1. **Initial Setup** - System hardening and basic security
2. **Services** - Service configuration and hardening
3. **Network** - Network security and configuration
4. **Firewall** - Host-based firewall setup
5. **Access Control** - User authentication and authorization
6. **Logging** - System logging and auditing
7. **Maintenance** - Ongoing security maintenance

**Usage:**
```bash
cd cis-ubuntu
# Run all phases
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml --ask-become-pass

# Run specific phase
ansible-playbook -i inventory/hosts.ini playbooks/phase1_initial_setup.yml --ask-become-pass

# Run with tags
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml --tags=critical --ask-become-pass
```

### NT542-report - Compliance Reporting

Security assessment tools and compliance reporting for CIS benchmark verification.

**Tools:**
- Lynis security scanning
- OpenSCAP compliance assessment
- Custom compliance checks
- Report generation

**Usage:**
```bash
cd cis-ubuntu
# Lynis scan
ansible-playbook -i inventory/hosts.ini playbooks/security_assessment_lynis.yml --ask-become-pass

# OpenSCAP scan
ansible-playbook -i inventory/hosts.ini playbooks/security_assessment_openscap.yml --ask-become-pass

# Comprehensive assessment
ansible-playbook -i inventory/hosts.ini playbooks/run_security_assessment.yml --ask-become-pass
```

## Configuration

### Inventory Configuration

Edit the inventory file to specify target systems:
```bash
nano cis-ubuntu/inventory/hosts.ini
```

Example:
```ini
[servers]
server1 ansible_host=192.168.1.10 ansible_user=ubuntu ansible_ssh_private_key_file=~/NT542
server2 ansible_host=192.168.1.11 ansible_user=ubuntu ansible_ssh_private_key_file=~/NT542
```

### Global Variables

Configure security settings:
```bash
nano cis-ubuntu/group_vars/all.yml
```

Key settings:
```yaml
# Password Policy
password_max_days: 90
password_min_length: 14

# Firewall
cis_firewall_type: "ufw"

# SSH
ssh_port: 22
```

## Safety and Recovery

### SSH Recovery
If SSH access is lost after hardening:
```bash
cd cis-ubuntu
ansible-playbook -i inventory/hosts.ini playbooks/ssh_recovery.yml --ask-become-pass
```

### Backup and Rollback
- Configuration files are automatically backed up
- All changes are logged for audit purposes
- Recovery playbooks available for critical services

## Results and Reports

All reports are stored in component-specific directories:
- VM logs: `auto-vm/logs/`
- Security reports: `cis-ubuntu/results/`
- Compliance reports: `NT542-report/reports/`

## Compliance Standards

This project implements:
- **CIS Ubuntu Linux 24.04 LTS Benchmark v1.0.0**
- **NIST Cybersecurity Framework**
- **Industry best practices**

## Troubleshooting

### Common Issues

1. **SSH Connection Issues**
   - Verify SSH key permissions: `chmod 600 ~/NT542`
   - Check network connectivity
   - Use recovery playbook if needed

2. **Permission Denied**
   - Ensure proper sudo configuration
   - Check Ansible user permissions

3. **VM Creation Fails**
   - Verify virtualization support
   - Check disk space
   - Review VM configuration

### Debug Mode
```bash
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml -vvv --ask-become-pass
```

## Development Workflow

1. **Setup Environment**: Configure SSH keys and inventory
2. **Create Test VMs**: Use auto-vm for testing environment
3. **Apply Hardening**: Run cis-ubuntu playbooks
4. **Verify Compliance**: Execute security assessments
5. **Review Reports**: Analyze compliance results
6. **Iterate**: Address findings and re-assess

## Security Considerations

- All sensitive data should be encrypted using Ansible Vault
- SSH keys should be protected with strong passphrases
- Test in non-production environments first
- Regular security assessments recommended
- Keep Ansible and system packages updated

## Contributing

When contributing to this project:
1. Follow CIS benchmark guidelines
2. Test changes thoroughly
3. Update documentation
4. Maintain security best practices
5. Use proper error handling

## License

This project follows CIS Ubuntu Linux Benchmark licensing requirements and is intended for educational and security testing purposes.

---

**Note**: Always test security hardening in a non-production environment before applying to production systems.
