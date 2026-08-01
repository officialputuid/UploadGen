# UploadGen

**UploadGen** adalah skrip Python yang serbaguna dirancang untuk menyederhanakan proses unggah dan unduh file ke platform berbagi file populer melalui antarmuka baris perintah yang intuitif.

## Fitur

- **Unggah ke 7 layanan**: Pixeldrain, Gofile, Bashupload, Devuploads, TmpFiles.org, Uguu, 0x0.st
- **Unduh file** dari URL dengan progress bar
- **Progress bar** real-time saat upload & download (`tqdm`)
- **Spinner animasi** saat proses jaringan (cek server, validasi API, cari link)
- **Tab completion** saat input path file
- **CLI & Interactive mode**

## Persyaratan

- Python 3.x
- Library: `requests`, `tqdm` (dapat diinstal melalui `pip`)

```bash
pip install -r requirements.txt
```

## Instalasi

```bash
git clone https://github.com/officialputuid/UploadGen.git
cd UploadGen
```

Atau unduh langsung:

```bash
wget https://raw.githubusercontent.com/officialputuid/UploadGen/main/uploadgen.py
```

Atau set sebagai ENV command:

```bash
sudo wget https://raw.githubusercontent.com/officialputuid/UploadGen/main/uploadgen.py -O /usr/local/bin/upg && sudo chmod +x /usr/local/bin/upg
```

## Penggunaan

### Interactive Mode

```bash
python3 uploadgen.py
```

### Upload via CLI

```bash
python3 uploadgen.py -s [1-7] -f [file]
```

| Flag | Layanan |
|------|---------|
| `-s 1` | Pixeldrain.com (API) |
| `-s 2` | Gofile.io |
| `-s 3` | Bashupload.app |
| `-s 4` | Devuploads.com (API) |
| `-s 5` | TmpFiles.org |
| `-s 6` | Uguu.se |
| `-s 7` | 0x0.st |

### Download via CLI

```bash
python3 uploadgen.py -d [URL] -o [output]
```

Contoh: `python3 uploadgen.py -d https://example.com/file.zip -o myfile.zip`

### ENV Command

```bash
upg                              # Interactive mode
upg -s 2 -f /path/file.txt       # Upload via CLI
upg -d https://url/file.zip      # Download via CLI
```

## 🌐 WebUI

Upload/download dari browser tanpa terminal — drag & drop file, pilih layanan, status server, riwayat job.

```bash
cd UploadGen
python3 -m venv venv && venv/bin/pip install flask -r requirements.txt  # sekali
./start-webui.sh                    # → http://127.0.0.1:5101
```

Akses dari jaringan lain: set `UPGEN_HOST=0.0.0.0` + `UPGEN_TOKEN` (atau file `webui/.token`), lihat `webui/README.md`.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.
