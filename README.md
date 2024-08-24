# UploadGen

**UploadGen** adalah skrip Python yang serbaguna dirancang untuk menyederhanakan proses unggah file ke platform berbagi file populer melalui antarmuka baris perintah yang intuitif.

## Fitur

- **Unggah ke Pixeldrain**: Memerlukan otentikasi kunci API untuk unggah file.
- **Unggah ke GoFile**: Secara otomatis memilih server yang sesuai untuk unggah.
- **Unggah ke Bashupload**: File disimpan selama 3 hari dan hanya dapat diunduh sekali.
- **Unggah ke Devuploads**: Memerlukan otentikasi kunci API untuk unggah file.

## Persyaratan

- Python 3.x
- Library `requests` (dapat diinstal melalui `pip`)

## Instalasi

Untuk memulai dengan UploadGen, ikuti langkah-langkah berikut:

   ```bash
   git clone https://github.com/officialputuid/UploadGen.git
   cd UploadGen
   pip install requests
   ```

Atau, Anda dapat mengunduh skrip secara langsung:

   ```bash
   wget https://github.com/officialputuid/UploadGen/raw/main/uploadgen.py
   pip install requests
   ```

## Penggunaan

1. **Interactive Mode**

Untuk menjalankan skrip dan menggunakan menu interaktif:

   ```bash
   python uploadgen.py
   ```

2. **Command-Line Arguments**

Untuk mengunggah file langsung menggunakan argumen baris perintah:

   ```bash
   python uploadgen.py -s [1/2/3/4] -f [file]
   ```
   contoh: `python uploadgen.py -s 1 -f /path/file.txt`

- `-h`: Panduan UploadGen
- `-s [1/2/3/4]`: Memilih layanan:
  - `1` untuk Pixeldrain
  - `2` untuk GoFile
  - `3` untuk Bashupload
  - `4` untuk Devuploads
- `-f [file]`: Menentukan jalur ke file yang ingin Anda unggah.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.
