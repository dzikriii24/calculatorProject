# Social Media Account Tracker

Program Python untuk melacak akun sosial media dan mengumpulkan informasi publik dari berbagai platform.

## ⚠️ DISCLAIMER PENTING

**Program ini hanya mengumpulkan informasi yang tersedia secara publik dan legal.**
- Selalu patuhi Terms of Service platform
- Hormati privasi pengguna lain
- Gunakan dengan bertanggung jawab dan legal
- Jangan gunakan untuk tujuan yang merugikan

## 🚀 Fitur

### 1. Social Media Tracker (`social_media_tracker.py`)
- Melacak akun di TikTok, Instagram, Twitter, YouTube, Facebook
- Mengumpulkan informasi profil publik
- Menyimpan hasil dalam format JSON

### 2. Advanced Tracker (`advanced_tracker.py`)
- Menggunakan Selenium untuk scraping yang lebih efektif
- Mendeteksi anti-bot measures
- Pencarian komentar dan interaksi
- Database SQLite untuk menyimpan data

### 3. Comment Tracker (`comment_tracker.py`)
- Melacak komentar dari username di berbagai platform
- Database SQLite untuk menyimpan komentar
- Generate laporan HTML
- Pencarian di TikTok, Instagram, Twitter, YouTube, Reddit

## 📋 Requirements

```bash
pip install -r requirements.txt
```

### Dependencies:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `selenium` - Web automation
- `undetected-chromedriver` - Anti-detection browser
- `lxml` - XML/HTML parser
- `html5lib` - HTML parser

## 🛠️ Instalasi

1. Clone atau download repository ini
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Chrome browser (untuk Selenium)
4. Jalankan program sesuai kebutuhan

## 📖 Cara Penggunaan

### 1. Basic Social Media Tracking

```bash
python social_media_tracker.py
```

Program akan:
- Mencari akun "gnkihhhhf" di semua platform
- Mengumpulkan informasi profil publik
- Menyimpan hasil dalam file JSON

### 2. Advanced Tracking dengan Selenium

```bash
python advanced_tracker.py
```

Program akan:
- Menggunakan browser automation
- Scraping yang lebih efektif
- Mencari komentar dan interaksi
- Menyimpan hasil dalam database

### 3. Comment Tracking

```bash
python comment_tracker.py
```

Program akan:
- Mencari komentar dari username di semua platform
- Menyimpan komentar dalam database SQLite
- Generate laporan HTML

## 🔧 Konfigurasi

### Mengubah Username Target

Edit file Python dan ubah variabel `username`:

```python
username = "gnkihhhhf"  # Ganti dengan username yang ingin dilacak
```

### Mengatur Platform

Edit daftar platform di fungsi `run_full_scan()`:

```python
platforms = ['tiktok', 'instagram', 'twitter', 'youtube', 'facebook']
```

### Mengatur Rate Limiting

Ubah delay antar request:

```python
time.sleep(2)  # Delay 2 detik antar request
```

## 📊 Output

### 1. JSON Results
- File: `tracking_results_[username]_[timestamp].json`
- Berisi informasi profil dari semua platform

### 2. Database SQLite
- File: `comments_[username].db`
- Berisi komentar yang ditemukan

### 3. HTML Report
- File: `comment_report_[username]_[timestamp].html`
- Laporan visual komentar yang ditemukan

## 🚨 Troubleshooting

### Error: Chrome Driver Not Found
```bash
# Install Chrome browser
# Program akan otomatis download ChromeDriver
```

### Error: Rate Limited
```bash
# Tambahkan delay lebih lama
time.sleep(5)  # Delay 5 detik
```

### Error: Platform Blocked
```bash
# Gunakan proxy atau VPN
# Atau gunakan mode requests-only
```

## 📝 Contoh Output

### Console Output
```
🔍 Social Media Account Tracker
========================================
Tracking username: gnkihhhhf
Starting scan...

📱 TIKTOK:
   ✅ Account found: https://www.tiktok.com/@gnkihhhhf
   👤 Display Name: GNKIHHHHF
   👥 Followers: 1,234
   📝 Bio: This is my bio...

📱 INSTAGRAM:
   ✅ Account found: https://www.instagram.com/gnkihhhhf/
   👤 Display Name: GNKIHHHHF
   👥 Followers: 5,678
   📝 Bio: Instagram bio...

📱 TWITTER:
   ❌ Account not found

📱 YOUTUBE:
   ✅ Account found: https://www.youtube.com/@gnkihhhhf
   👤 Display Name: GNKIHHHHF
   👥 Subscribers: 987
```

### JSON Output
```json
{
  "username": "gnkihhhhf",
  "timestamp": "2024-01-15T10:30:00",
  "platforms": {
    "tiktok": {
      "status": "found",
      "url": "https://www.tiktok.com/@gnkihhhhf",
      "profile_data": {
        "display_name": "GNKIHHHHF",
        "follower_count": 1234,
        "following_count": 567,
        "video_count": 89,
        "verified": false,
        "bio": "This is my bio..."
      }
    }
  }
}
```

## 🔒 Keamanan dan Privasi

1. **Data Publik Only**: Program hanya mengumpulkan data yang tersedia secara publik
2. **No Personal Info**: Tidak mengumpulkan email, nomor telepon, atau data pribadi
3. **Respect ToS**: Patuhi Terms of Service setiap platform
4. **Rate Limiting**: Menggunakan delay untuk menghindari overload server

## ⚖️ Legal Considerations

- **Terms of Service**: Pastikan penggunaan sesuai dengan ToS platform
- **Privacy Laws**: Patuhi undang-undang privasi yang berlaku
- **Ethical Use**: Gunakan untuk tujuan yang legal dan etis
- **No Harassment**: Jangan gunakan untuk mengganggu atau melecehkan

## 🤝 Contributing

1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## 📄 License

Program ini dibuat untuk tujuan edukasi dan penelitian. Gunakan dengan bertanggung jawab.

## 🆘 Support

Jika mengalami masalah:
1. Cek troubleshooting section
2. Pastikan semua dependencies terinstall
3. Cek koneksi internet
4. Pastikan Chrome browser terinstall

## 🔄 Updates

- v1.0: Basic social media tracking
- v1.1: Added Selenium support
- v1.2: Added comment tracking
- v1.3: Added database support
- v1.4: Added HTML reporting

---

**Ingat: Gunakan program ini dengan bijak dan legal!**