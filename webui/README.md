# UploadGen WebUI

Antarmuka web lokal untuk UploadGen — upload/download file dari browser tanpa terminal.

## Menjalankan

```bash
cd ~/UploadGen
./start-webui.sh          # port default 5101
# atau custom port:
./start-webui.sh 8080
# atau langsung:
venv/bin/python webui/app.py
```

Buka **http://127.0.0.1:5101**

## Struktur

```
webui/
├── app.py            # Flask backend (reuse uploadgen.py asli, tanpa modifikasi)
├── templates/
│   └── index.html    # Frontend single-page (material white, frosted glass header)
├── uploads/          # file sementara upload (auto-hapus setelah sukses / 24 jam)
└── downloads/        # hasil download
```

## Akses dari browser (NAT / LAN)

Server bind **0.0.0.0** + proteksi token (wajib). Token tersimpan di `webui/.token`.

- **Di jaringan yang sama (rumah/kantor)**: buka `http://127.0.0.1:5101/?token=1a2b3c4d5e6f7g`
- **Dari luar**: SSH tunnel dulu, lalu buka `http://127.0.0.1:5101/?token=1a2b3c4d5e6f7g`
  ```
  ssh -L 5101:127.0.0.1:5101 root@ip-vps
  ```
- **Akses langsung dari internet**: forward port 5101 ke http://127.0.0.1 di router (pola sama seperti :5100).

Tanpa token benar → halaman login/401. Token bisa diganti dengan env UPGEN_TOKEN (file `webui/.token` hanya fallback).
