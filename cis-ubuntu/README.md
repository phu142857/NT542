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

## Cấu trúc

```
cis-ubuntu/
├── playbooks/
│   ├── site.yml                 # Main playbook with all roles
│   ├── audit.yml               # Compliance scan only
│   └── comprehensive_scan.yml  # Complete system scan
├── roles/
│   ├── system_info/            # System information gathering
│   ├── compliance_scan/        # Lynis + OpenSCAP scanning
│   └── [other CIS roles...]
└── README.md
```

## Sử dụng

### Chạy full CIS benchmark với thu thập thông tin hệ thống:
```bash
ansible-playbook -i inventory/hosts playbooks/site.yml
```

### Chạy comprehensive scan (khuyến khích):
```bash
ansible-playbook -i inventory/hosts playbooks/comprehensive_scan.yml
```

### Chạy chỉ compliance scan:
```bash
ansible-playbook -i inventory/hosts playbooks/audit.yml
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