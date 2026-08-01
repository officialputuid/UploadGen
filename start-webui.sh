#!/usr/bin/env bash
# UploadGen WebUI — start script
# Usage:
#   ./start-webui.sh [port]                # lokal (127.0.0.1)
#   UPGEN_HOST=0.0.0.0 ./start-webui.sh    # akses dari IP VPS (wajib set UPGEN_TOKEN!)
#   UPGEN_TOKEN=isi-token UPGEN_HOST=0.0.0.0 ./start-webui.sh 5101
set -e
cd "$(dirname "$0")"
PORT="${1:-5101}"
if [ ! -x venv/bin/python ]; then
  echo "[!] venv tidak ada. Buat dulu: python3 -m venv venv && venv/bin/pip install -r requirements.txt flask"
  exit 1
fi
if [ "${UPGEN_HOST:-127.0.0.1}" != "127.0.0.1" ] && [ -z "$UPGEN_TOKEN" ]; then
  echo "[!] Bind ke 0.0.0.0 WAJIB pakai UPGEN_TOKEN biar nggak jadi uploader publik."
  echo "    Contoh: UPGEN_TOKEN=<token-acak> UPGEN_HOST=0.0.0.0 $0 $PORT"
  exit 1
fi
echo "UploadGen WebUI → http://${UPGEN_HOST:-127.0.0.1}:${PORT}"
UPGEN_PORT="$PORT" UPGEN_HOST="${UPGEN_HOST:-127.0.0.1}" exec venv/bin/python webui/app.py
