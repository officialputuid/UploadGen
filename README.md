# UploadGen

**UploadGen** adalah skrip Python yang serbaguna dirancang untuk menyederhanakan proses unggah file ke platform berbagi file populer melalui antarmuka baris perintah yang intuitif. [EN](README-en.md)

## Fitur

- **Unggah ke Pixeldrain.com**
- **Unggah ke GoFile.io**
- **Unggah ke Bashupload.com**
- **Unggah ke Devuploads.com**
- **Unggah ke File.io**
- **Unggah ke Uguu.se**

## Persyaratan

- Python 3.x
- Library `requests` (dapat diinstal melalui `pip`)

## Instalasi

Untuk memulai dengan UploadGen, ikuti langkah-langkah berikut:

   ```bash
   git clone https://github.com/officialputuid/UploadGen.git
   cd UploadGen
   python3 uploadgen.py or python uploadgen.py -s [1/2/3/4/5/6] -f [file]
   ```

Atau, Anda dapat mengunduh skrip secara langsung:

   ```bash
   wget https://raw.githubusercontent.com/officialputuid/UploadGen/main/uploadgen.py
   python3 uploadgen.py / python uploadgen.py -s [1/2/3/4/5/6] -f [file]
   ```

## Penggunaan

1. **Interactive Mode**

Untuk menjalankan skrip dan menggunakan menu interaktif:

   ```bash
   python3 uploadgen.py
   ```

2. **Command-Line Arguments**

Untuk mengunggah file langsung menggunakan argumen baris perintah:

   ```bash
   python3 uploadgen.py -s [1/2/3/4/5/6] -f [file]
   ```
   contoh: `python uploadgen.py -s 2 -f /path/file.txt`

- `-h`: Panduan UploadGen
- `-s [1/2/3/4/5/6]`: Memilih layanan:
  - `1` untuk Pixeldrain.com
  - `2` untuk GoFile.io
  - `3` untuk Bashupload.com
  - `4` untuk Devuploads.com
  - `5` untuk File.io
  - `6` untuk Uguu.se
- `-f [file]`: Menentukan jalur ke file yang ingin Anda unggah.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.
