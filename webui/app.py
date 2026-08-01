#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UploadGen WebUI — antarmuka web lokal untuk UploadGen v2.2
Menjalankan semua layanan upload/download dari uploadgen.py lewat browser.

Run:
    cd ~/UploadGen/webui
    ../venv/bin/python app.py
Buka:  http://127.0.0.1:5101  (ubah port: UPGEN_PORT=xxxx)
"""

import os
import re
import sys
import json
import time
import uuid
import queue
import threading
import subprocess
from pathlib import Path

from flask import Flask, request, jsonify, Response, render_template

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
UPLOAD_DIR = BASE_DIR / "uploads"
DOWNLOAD_DIR = BASE_DIR / "downloads"
UPLOAD_DIR.mkdir(exist_ok=True)
DOWNLOAD_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT_DIR))
import uploadgen as ug  # noqa: E402  (reuse layanan asli)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 * 1024  # 2 GB

HOST = os.environ.get("UPGEN_HOST", "127.0.0.1")
PORT = int(os.environ.get("UPGEN_PORT", "5101"))
TOKEN = os.environ.get("UPGEN_TOKEN", "").strip()
if not TOKEN:
    _tf = Path(__file__).resolve().parent / ".token"
    if _tf.exists():
        TOKEN = _tf.read_text().strip()

JOBS = {}
JOBS_LOCK = threading.Lock()
HISTORY = []
HISTORY_LOCK = threading.Lock()
MAX_HISTORY = 50

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")  # semua CSI escape
FAIL_PAT = re.compile(r"gagal|error|tidak valid|tidak ditemukan|kunci api", re.I)
SPINNERS = set("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")

# Runner: jalankan fungsi upload asli tanpa banner & tanpa health-check tambahan
RUN_UPLOAD = r'''
import sys
import uploadgen as ug

sid = int(sys.argv[1])
path = sys.argv[2]
key = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None

info = ug.SERVICES[sid]
print(f"[{info['name']}] Mulai unggah ...")
if info["needs_api"]:
    if not key:
        print("ERROR: API key dibutuhkan untuk layanan ini")
        sys.exit(1)
    info["fn"](key, path)
else:
    info["fn"](path)
'''

RUN_DOWNLOAD = r'''
import sys
import uploadgen as ug

url = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None
ug.download_file(url, out)
'''


def safe_name(name):
    """Sanitasi nama file (cegah path traversal)."""
    name = os.path.basename(str(name).replace("\\", "/"))
    name = re.sub(r"[^\w.\-() ]", "_", name).strip(" .")
    return name or "file"


def clean_line(raw):
    """Bersihkan ANSI, buang bar tqdm & frame spinner, return line atau None."""
    s = ANSI_RE.sub("", raw).strip()
    if not s:
        return None
    if s[0] in SPINNERS:
        return None
    if "%|" in s:  # progress bar tqdm — ditampilkan lewat bar, bukan log
        return None
    return s


def purge_old_files(hours=24):
    """Hapus file sementara yang lebih tua dari N jam."""
    cutoff = time.time() - hours * 3600
    for folder in (UPLOAD_DIR, DOWNLOAD_DIR):
        try:
            for p in folder.iterdir():
                if p.is_file() and p.stat().st_mtime < cutoff:
                    p.unlink(missing_ok=True)
        except OSError:
            pass


def new_job(job_type, label):
    job = {
        "id": uuid.uuid4().hex,
        "type": job_type,
        "label": label,
        "q": queue.Queue(),
        "lines": [],
        "percent": 0,
        "done": False,
        "result": None,
        "created": time.time(),
    }
    with JOBS_LOCK:
        JOBS[job["id"]] = job
    return job


def reader_thread(job, proc, job_type, extra=None):
    """Baca stdout/stderr subprocess → queue SSE; selesaikan job."""
    last_percent = 0
    try:
        for raw in proc.stdout:
            for seg in raw.split("\r"):
                seg = ANSI_RE.sub("", seg).strip()
                if not seg:
                    continue
                if seg[0] in SPINNERS:
                    continue
                m = re.search(r"(\d+)%\|", seg)
                if m:
                    last_percent = int(m.group(1))
                    job["percent"] = last_percent
                    job["q"].put(("progress", last_percent))
                    continue
                if "%|" in seg:
                    continue
                job["lines"].append(seg)
                job["q"].put(("log", seg))
    except Exception as e:  # pragma: no cover
        job["lines"].append(f"reader error: {e}")
    finally:
        proc.wait()

    job["result"] = parse_result(job_type, proc, job["lines"], extra)
    job["done"] = True
    job["q"].put(("done", job["result"]))

    # cleanup file sementara upload yang sukses
    if job_type == "upload" and job["result"].get("ok"):
        try:
            Path(extra["dest"]).unlink(missing_ok=True)
        except OSError:
            pass

    with HISTORY_LOCK:
        HISTORY.append({
            "id": job["id"],
            "type": job_type,
            "label": job["label"],
            "ok": job["result"].get("ok"),
            "link": job["result"].get("link"),
            "path": job["result"].get("path"),
            "error": job["result"].get("error"),
            "ts": time.strftime("%H:%M:%S"),
        })
        del HISTORY[:-MAX_HISTORY]


def parse_result(job_type, proc, lines, extra):
    text = "\n".join(lines)
    if job_type == "upload":
        failed = any(FAIL_PAT.search(l) for l in lines)
        links = re.findall(r"https?://[^\s'\"]+", text)
        if proc.returncode == 0 and not failed and links:
            # ambil link dari baris sukses terakhir (bukan baris error)
            for l in reversed(lines):
                m = re.search(r"https?://[^\s'\"]+", l)
                if m:
                    return {"ok": True, "link": m.group(0), "service": extra.get("service")}
        err = next(
            (l for l in reversed(lines) if FAIL_PAT.search(l)),
            lines[-1] if lines else "Gagal mengunggah",
        )
        return {"ok": False, "error": err}
    # download
    dest = extra.get("dest")
    if proc.returncode == 0 and dest and dest.exists() and dest.stat().st_size > 0:
        return {"ok": True, "path": str(dest), "name": dest.name,
                "size": ug.fmt_size(dest.stat().st_size)}
    err = next(
        (l for l in reversed(lines) if FAIL_PAT.search(l)),
        lines[-1] if lines else "Gagal mengunduh",
    )
    return {"ok": False, "error": err}


# ── Routes ────────────────────────────────────────────────────────────────
LOGIN_PAGE = """<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UploadGen — Masuk</title>
<style>
body{font-family:'Google Sans','Segoe UI',system-ui,sans-serif;background:#fff;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;color:#202124}
.box{width:320px;padding:32px;border:1px solid #e8eaed;border-radius:16px;box-shadow:0 1px 3px rgba(60,64,67,.12)}
h1{font-size:18px;margin:0 0 6px}
p{font-size:13px;color:#5f6368;margin:0 0 18px}
input{width:100%;padding:12px 14px;border:1.5px solid #dadce0;border-radius:10px;font-size:14px;outline:none;box-sizing:border-box}
input:focus{border-color:#1a73e8;box-shadow:0 0 0 3px rgba(26,115,232,.15)}
button{width:100%;margin-top:14px;padding:12px;background:#1a73e8;color:#fff;border:none;border-radius:999px;font-size:14px;font-weight:600;cursor:pointer}
button:hover{background:#1765cc}
.err{color:#d93025;font-size:12.5px;margin-top:10px}
</style></head><body>
<div class="box">
<h1>🔒 UploadGen WebUI</h1>
<p>Server ini diproteksi. Masukkan token akses untuk lanjut.</p>
<form method="get" action="/">
<input type="password" name="token" placeholder="Token akses" autofocus autocomplete="off">
<button type="submit">Masuk</button>
</form>
<div class="err" id="e"></div>
</div>
<script>if(new URLSearchParams(location.search).get('token')===''){document.getElementById('e').textContent='Token salah atau kosong.';}</script>
</body></html>"""


@app.before_request
def check_token():
    if not TOKEN:
        return None
    supplied = request.args.get("token", "") or request.headers.get("X-Token", "")
    if supplied == TOKEN:
        return None
    if request.path == "/":
        return Response(LOGIN_PAGE, mimetype="text/html")
    return jsonify({"error": "Unauthorized"}), 401


@app.get("/")
def index():
    return render_template("index.html", services=ug.SERVICES)


@app.get("/api/status")
def api_status():
    results = ug.check_all_services()
    items = []
    for sid, info in ug.SERVICES.items():
        items.append({
            "id": sid,
            "name": info["name"],
            "needs_api": info["needs_api"],
            "url": info["url"],
            "online": bool(results.get(sid, False)),
        })
    online = sum(1 for i in items if i["online"])
    return jsonify({"services": items, "online": online, "total": len(items)})


@app.post("/api/upload")
def api_upload():
    purge_old_files()
    f = request.files.get("file")
    service = request.form.get("service", "")
    api_key = request.form.get("api_key", "").strip()

    if not f or not f.filename:
        return jsonify({"error": "File belum dipilih"}), 400
    try:
        sid = int(service)
        info = ug.SERVICES[sid]
    except (ValueError, KeyError):
        return jsonify({"error": "Layanan tidak valid"}), 400
    if info["needs_api"] and not api_key:
        return jsonify({"error": f"{info['name']} butuh API key"}), 400

    dest = UPLOAD_DIR / f"{uuid.uuid4().hex[:8]}_{safe_name(f.filename)}"
    f.save(dest)

    job = new_job("upload", safe_name(f.filename))
    cmd = [sys.executable, "-c", RUN_UPLOAD, str(sid), str(dest), api_key]
    proc = subprocess.Popen(
        cmd, cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )
    threading.Thread(
        target=reader_thread, args=(job, proc, "upload"),
        kwargs={"extra": {"dest": dest, "service": info["name"]}},
        daemon=True,
    ).start()
    return jsonify({"job_id": job["id"], "service": info["name"], "file": job["label"]})


@app.post("/api/download")
def api_download():
    purge_old_files()
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "URL kosong"}), 400

    out_name = safe_name(data.get("output") or os.path.basename(url.split("?")[0]) or "downloaded_file")
    dest = DOWNLOAD_DIR / out_name
    if dest.exists():
        dest = DOWNLOAD_DIR / f"{uuid.uuid4().hex[:6]}_{out_name}"

    job = new_job("download", url)
    cmd = [sys.executable, "-c", RUN_DOWNLOAD, url, str(dest)]
    proc = subprocess.Popen(
        cmd, cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )
    threading.Thread(
        target=reader_thread, args=(job, proc, "download"),
        kwargs={"extra": {"dest": dest}},
        daemon=True,
    ).start()
    return jsonify({"job_id": job["id"], "url": url, "output": dest.name})


@app.get("/api/job/<job_id>")
def job_stream(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "Job tidak ditemukan"}), 404

    def gen():
        yield "retry: 3000\n\n"
        while True:
            try:
                evt, data = job["q"].get(timeout=15)
            except queue.Empty:
                if job["done"]:
                    yield f"event: done\ndata: {json.dumps(job['result'])}\n\n"
                    return
                yield ": keepalive\n\n"
                continue
            if evt == "log":
                yield f"event: log\ndata: {json.dumps({'line': data, 'percent': job['percent']})}\n\n"
            elif evt == "progress":
                yield f"event: progress\ndata: {json.dumps({'percent': data})}\n\n"
            elif evt == "done":
                yield f"event: done\ndata: {json.dumps(data)}\n\n"
                return

    return Response(gen(), mimetype="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    })


@app.get("/api/history")
def api_history():
    with HISTORY_LOCK:
        return jsonify({"jobs": list(reversed(HISTORY))})


@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "File terlalu besar (maks 2 GB)"}), 413


if __name__ == "__main__":
    print(f"UploadGen WebUI → http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, threaded=True, debug=False)
