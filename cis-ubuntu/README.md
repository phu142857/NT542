# CIS Ubuntu Benchmark System

Hệ thống đánh giá tuân thủ CIS benchmark cho Ubuntu với tích hợp OpenSCAP và thu thập thông tin hệ thống.

## Các tính năng

### 1. Thu thập thông tin hệ thống (System Info)
- **CPU**: Model name, tốc độ, số cores, threads, vendor ID, load average
- **RAM**: Tổng dung lượng, đã sử dụng, còn trống, thông tin swap
- **Ổ cứng**: Model, kích thước, loại (HDD/SSD), SMART status, disk usage
- **Network**: Interfaces, địa chỉ IP, thống kê mạng
- **Display/GPU**: Thông tin VGA, NVIDIA GPU details (nếu có)
- **System Overview**: Hostname, kernel, OS, uptime, last boot

### 2. OpenSCAP Integration
- Cài đặt OpenSCAP và SCAP Security Guide
- Tải CIS benchmark profile cho Ubuntu 22.04
- Thực hiện scan với CIS benchmark
- Tạo báo cáo XML và HTML
- Tự động fallback sang standard profile nếu CIS profile không khả dụng

### 3. Lynis Audit
- Thực hiện audit nhanh hệ thống
- Tạo báo cáo security recommendations
- Tích hợp với báo cáo tổng hợp

## Cấu trúc theo Phase

Dự án được tổ chức theo 8 phase tương ứng với các giai đoạn hardening theo CIS Benchmark:

```
cis-ubuntu/
├── playbooks/
│   ├── site.yml                 # Main playbook với tất cả phases
│   ├── phase_1.yml             # Phase 1: Initial Setup
│   ├── phase_2.yml             # Phase 2: Filesystem Configuration
│   ├── phase_3.yml             # Phase 3: Password and Authentication
│   ├── phase_4.yml             # Phase 4: SSH Configuration
│   ├── phase_5.yml             # Phase 5: Services Configuration
│   ├── phase_6.yml             # Phase 6: Network and Firewall
│   ├── phase_7.yml             # Phase 7: Logging and Audit
│   ├── phase_8.yml             # Phase 8: Compliance and Verification
│   ├── audit.yml               # Compliance scan only
│   └── comprehensive_scan.yml  # Complete system scan
├── roles/
│   ├── phase_1/                # Initial Setup and System Information
│   │   ├── system_info/
│   │   └── packages/
│   ├── phase_2/                # Filesystem Configuration
│   │   ├── filesystem/
│   │   └── system_settings/
│   ├── phase_3/                # Password and Authentication
│   │   └── password_policy/
│   ├── phase_4/                # SSH Configuration
│   │   └── ssh/
│   ├── phase_5/                # Services Configuration
│   │   └── services/
│   ├── phase_6/                # Network and Firewall
│   │   ├── network/
│   │   └── firewall/
│   ├── phase_7/                # Logging and Audit
│   │   └── logging_audit/
│   ├── phase_8/                # Compliance and Verification
│   │   └── compliance_scan/
│   └── README.md
└── README.md
```

## Sử dụng

### Triển khai theo từng phase:

#### Phase 1: Initial Setup and System Information
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_1.yml
```

#### Phase 2: Filesystem Configuration
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_2.yml
```

#### Phase 3: Password and Authentication
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_3.yml
```

#### Phase 4: SSH Configuration
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_4.yml
```

#### Phase 5: Services Configuration
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_5.yml
```

#### Phase 6: Network and Firewall
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_6.yml
```

#### Phase 7: Logging and Audit
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_7.yml
```

#### Phase 8: Compliance and Verification
```bash
ansible-playbook -i inventory/hosts.ini playbooks/phase_8.yml
```

### Triển khai tuần tự tất cả phases:
```bash
# Triển khai tuần tự từ phase 1 đến 8
for i in {1..8}; do
    echo "Deploying Phase $i..."
    ansible-playbook -i inventory/hosts.ini playbooks/phase_$i.yml
done
```

### Chạy full CIS benchmark với thu thập thông tin hệ thống:
```bash
ansible-playbook -i inventory/hosts.ini playbooks/site.yml
```

## Files được tạo ra

### System Information
- `/tmp/cis_system_info_report.txt` - Báo cáo thông tin hệ thống đầy đủ
- `/var/log/cis_benchmark/cis_system_info_report.txt` - Bản lưu persist

### Compliance Reports
- `/tmp/lynis_report.txt` - Kết quả Lynis audit
- `/tmp/openscap_results.xml` - Kết quả OpenSCAP XML
- `/tmp/openscap_report.html` - Báo cáo OpenSCAP HTML
- `/tmp/openscap_summary.txt` - Tóm tắt OpenSCAP
- `/tmp/comprehensive_compliance_report.txt` - Báo cáo tuân thủ tổng hợp

### Final Report
- `/tmp/final_comprehensive_report.txt` - Báo cáo cuối cùng kết hợp tất cả
- `/var/log/cis_benchmark/` - Thư mục lưu persist tất cả reports

## Yêu cầu hệ thống

- Ubuntu 20.04/22.04
- Ansible 2.9+
- Internet connection (cho download CIS benchmark)
- Quyền root/sudo

## OpenSCAP Profiles

- **CIS Profile**: `xccdf_org.ssgproject.content_profile_cis`
- **Standard Profile**: `xccdf_org.ssgproject.content_profile_standard` (fallback)

## Example Output

Báo cáo sẽ bao gồm:
1. System overview và hardware information
2. Lynis security audit results
3. OpenSCAP compliance scan với CIS benchmark
4. HTML report cho easy viewing
5. Recommendations và next steps

## Troubleshooting

- Nếu OpenSCAP scan thất bại, kiểm tra package installation
- Nếu CIS benchmark không download được, system sẽ tự động dùng standard profile
- SMART status chỉ available nếu `smartmontools` được cài đặt
- NVIDIA GPU info chỉ available nếu NVIDIA drivers được cài đặt