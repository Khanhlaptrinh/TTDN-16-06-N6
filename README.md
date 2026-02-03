<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    Youth Union Member Management
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Hệ thống Quản lý tài sản và Phòng họp được xây dựng nhằm số hóa công tác quản lý phòng họp và tài sản dùng chung trong đơn vị, tích hợp với module Quản lý nhân sự. Hệ thống cho phép theo dõi thông tin phòng họp, tài sản, nhân viên sử dụng, lịch sử đặt phòng và kiểm soát trùng lịch, giúp tối ưu việc sử dụng tài nguyên và nâng cao hiệu quả quản lý.

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/en-us/windows/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

### Công nghệ chính
[![XML](https://img.shields.io/badge/XML-0060AC?style=for-the-badge&logo=xml&logoColor=white)](https://www.w3.org/XML/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)


### Database Management Tools
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🚀 3. Hình ảnh các chức năng
<div align="center">
  <p><strong>1. Quản lý phòng họp</strong></p>
  <table>
    <tr>
      <td align="center">
        <img src="docs/screenshots/giao_dien_quan_ly_phong.png" alt="QuanLyPhong" width="300"><br>
        <sub>Quản lý phòng</sub>
      </td>
      <td align="center">
        <img src="docs/screenshots/Quan_ly_phong_hop1.png" alt="TaoPhongHop" width="300"><br>
        <sub>Tạo phòng họp</sub>
      </td>
    </tr>
  </table>
</div>

<div align="center">
  <p><strong>2. Quản lý tài sản</strong></p>
  <table>
    <tr>
      <td align="center">
        <img src="docs/screenshots/giao_dien_quan_ly_tai_san.png" alt="QuanLyTaiSan" width="300"><br>
        <sub>Quản lý tài sản</sub>
      </td>
      <td align="center">
        <img src="docs/screenshots/tao_tai_san.png" alt="TaoTaiSan" width="300"><br>
        <sub>Tạo tài sản</sub>
      </td>
      <td align="center">
        <img src="docs/screenshots/quan_ly_muon_tra.png" alt="QuanLyMuonTra" width="300"><br>
        <sub>Quản lý mượn trả</sub>
      </td>
      <td align="center">
        <img src="docs/screenshots/lich_su_cap_phat.png" alt="LichSuCapPhat" width="300"><br>
        <sub>Lịch sử cấp phát</sub>
      </td>
    </tr>
  </table>
</div>

<div align="center">
  <p><strong>3. External API</strong></p>
  <table>
    <tr>
      <td align="center">
        <img src="docs/screenshots/quan_ly_dat_phong1.png" alt="QuanLyTaiSan" width="300"><br>
        <sub>Quản lý tài sản</sub>
      </td>
      <td align="center">
        <img src="docs/screenshots/quan_ly_tai_san.png" alt="TaoTaiSan" width="300"><br>
        <sub>Tạo tài sản</sub>
      </td>
      <td align="center">
        <img src="docs/screenshots/quan_ly_phong_hop.png" alt="LichSuCapPhat" width="300"><br>
        <sub>Lịch sử cấp phát</sub>
      </td>
    </tr>
  </table>
</div>

### 4. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 4.1.1. Clone project.
https://github.com/Khanhlaptrinh/TTDN-16-06-N6.git

## 4.1.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 4.1.3. khởi tạo môi trường ảo.

`python3.10 -m venv ./venv`
Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
pip3 install -r requirements.txt
```

# 4.2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.

`sudo docker-compose up -d`

# 4.3. Setup tham số chạy cho hệ thống

## 4.3.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5432
xmlrpc_port = 8069
```
Có thể kế thừa từ **odoo.conf.template**

Ngoài ra có thể thêm mổ số parameters như:

```
-c _<đường dẫn đến tệp odoo.conf>_
-u _<tên addons>_ giúp cập nhật addons đó trước khi khởi chạy
-d _<tên database>_ giúp chỉ rõ tên database được sử dụng
--dev=all giúp bật chế độ nhà phát triển 
```

# 4.4. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất
    
python3 odoo-bin.py -c odoo.conf -u all
