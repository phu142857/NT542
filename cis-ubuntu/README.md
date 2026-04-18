# CIS Ubuntu Linux 24.04 LTS Hardening

This directory contains Ansible playbooks and roles to implement the CIS Ubuntu Linux 24.04 LTS Benchmark v1.0.0 security hardening guidelines.

## Overview

The CIS Ubuntu hardening automation is organized into 7 phases that systematically secure Ubuntu systems according to industry best practices:

- **Phase 1**: Initial Setup & System Hardening
- **Phase 2**: Services Configuration
- **Phase 3**: Network Configuration
- **Phase 4**: Host-Based Firewall
- **Phase 5**: Access Control
- **Phase 6**: Logging and Auditing
- **Phase 7**: System Maintenance

## Directory Structure

```
cis-ubuntu/
|-- ansible.cfg                 # Ansible configuration
|-- group_vars/
|   |-- all.yml                # Global variables (password policy, firewall settings)
|-- inventory/
|   |-- hosts.ini              # Target server inventory
|-- playbooks/                 # Main execution playbooks
|   |-- phase1_initial_setup.yml
|   |-- phase2_services.yml
|   |-- phase3_network.yml
|   |-- phase4_firewall.yml
|   |-- phase5_access_control.yml
|   |-- phase6_logging_auditing.yml
|   |-- phase7_system_maintenance.yml
|   |-- run_all_phases.yml     # Execute all phases
|   |-- run_security_assessment.yml
|   |-- security_assessment_lynis.yml
|   |-- security_assessment_openscap.yml
|   |-- ssh_recovery.yml       # Emergency SSH access recovery
|-- roles/                      # Implementation roles for each phase
|   |-- phase1_initial_setup/
|   |-- phase2_services/
|   |-- phase3_network/
|   |-- phase4_firewall/
|   |-- phase5_access_control/
|   |-- phase6_logging_auditing/
|   |-- phase7_system_maintenance/
|-- results/                    # Scan results and reports
|-- scripts/                    # Utility scripts
```

## Quick Start

### Prerequisites
- Ansible 2.9+ installed on control node
- SSH key-based authentication configured
- Target servers running Ubuntu 24.04 LTS
- Python3 installed on target servers

### Configuration

1. **Edit inventory file:**
   ```bash
   nano inventory/hosts.ini
   ```

2. **Configure global variables:**
   ```bash
   nano group_vars/all.yml
   ```

### Running the Hardening

#### Option 1: Run All Phases (Recommended)
```bash
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml --ask-become-pass
```

#### Option 2: Run Individual Phases
```bash
# Phase 1 - Initial Setup
ansible-playbook -i inventory/hosts.ini playbooks/phase1_initial_setup.yml --ask-become-pass

# Phase 2 - Services
ansible-playbook -i inventory/hosts.ini playbooks/phase2_services.yml --ask-become-pass

# Continue with remaining phases...
```

#### Option 3: Run with Tags
```bash
# Run only critical security tasks
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml --tags=critical --ask-become-pass

# Run only important tasks
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml --tags=important --ask-become-pass
```

## Security Assessment

After hardening, run security assessments to verify compliance:

### Lynis Security Scan
```bash
ansible-playbook -i inventory/hosts.ini playbooks/security_assessment_lynis.yml --ask-become-pass
```

### OpenSCAP Scan
```bash
ansible-playbook -i inventory/hosts.ini playbooks/security_assessment_openscap.yml --ask-become-pass
```

### Comprehensive Assessment
```bash
ansible-playbook -i inventory/hosts.ini playbooks/run_security_assessment.yml --ask-become-pass
```

## Phase Details

### Phase 1: Initial Setup
- Filesystem security configuration
- Kernel parameter hardening
- AppArmor configuration
- Boot loader security
- System package cleanup

### Phase 2: Services
- Disable unnecessary services
- Configure time synchronization
- Set up fail2ban
- Mail system configuration
- Cron job security

### Phase 3: Network
- IPv6 configuration
- Wireless network disabling
- Network kernel module hardening
- TCP/IP stack security

### Phase 4: Firewall
- UFW/iptables/nftables configuration
- Outbound connection rules
- Firewall rule management
- Logging configuration

### Phase 5: Access Control
- SSH hardening
- PAM security configuration
- Sudoers configuration
- User account security
- Password policy enforcement

### Phase 6: Logging & Auditing
- System logging configuration
- Audit rule setup
- Log rotation
- File integrity monitoring
- Advanced audit rules

### Phase 7: System Maintenance
- File permissions review
- SUID/SGID file management
- World-writable file cleanup
- User/group integrity checks
- Home directory security

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
- **Handler Integration**: Fixed handler import issues for reliable service management

## Recent Improvements

### Fixed Issues
- **Handler Import**: Resolved "handler not found" errors by properly importing handlers from all phases
- **IP Extraction**: Enhanced regex pattern for accurate IP address extraction from VMs
- **Inventory Management**: Automatic VM IP addition with duplicate prevention
- **Service Reliability**: Improved service restart handlers for logging and auditing tasks

## Results and Reports

All scan results and compliance reports are stored in the `results/` directory:
- Lynis reports: `results/<hostname>/lynis-report-<timestamp>.html`
- OpenSCAP reports: `results/<hostname>/openscap-report-<timestamp>.html`
- Log files: `results/<hostname>/`

## Variables

Key configurable variables in `group_vars/all.yml`:

```yaml
# Password Policy
password_max_days: 90
password_min_days: 7
password_warn_days: 7
password_min_length: 14

# Firewall Configuration
cis_firewall_type: "ufw"  # Options: ufw, iptables, nftables

# SSH Configuration
ssh_port: 22
```

## Safety Features

- **Backup Creation**: Important configuration files are backed up before modification
- **Validation**: System validates changes before applying
- **Rollback**: SSH recovery playbook available if access is lost
- **Logging**: All actions are logged for audit purposes

## Compliance

This implementation follows:
- CIS Ubuntu Linux 24.04 LTS Benchmark v1.0.0
- NIST Cybersecurity Framework guidelines
- Industry best practices for system hardening

## Troubleshooting

### Common Issues

1. **SSH Connection Lost**: Use `ssh_recovery.yml` playbook
2. **Service Failures**: Check logs in `/var/log/ansible/`
3. **Permission Denied**: Ensure proper SSH key setup
4. **Package Installation**: Verify internet connectivity

### Debug Mode
```bash
ansible-playbook -i inventory/hosts.ini playbooks/run_all_phases.yml -vvv --ask-become-pass
```

## Contributing

When adding new security controls:
1. Follow CIS benchmark guidelines
2. Test in non-production environment first
3. Include proper error handling
4. Add appropriate logging
5. Update documentation

## License

This project follows the CIS Ubuntu Linux Benchmark licensing requirements.
