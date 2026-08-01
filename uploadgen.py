#!/usr/bin/env python3

# Copyright (C) 2025 officialputuid
# UploadGen v2.2 — File uploader/downloader with progress bar & tab completion

import os
import re
import sys
import time
import glob
import argparse
import threading
import requests
import base64
import readline
from tqdm import tqdm

# ── Colors ──────────────────────────────────────────────────────────────────
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


# ── Progress file wrapper ───────────────────────────────────────────────────
class ProgressReader:
    """Wrap a file object with tqdm progress bar for uploads."""

    def __init__(self, fileobj, filepath, desc="Upload"):
        self.f = fileobj
        self.size = os.path.getsize(filepath)
        self.pbar = tqdm(
            total=self.size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"  {desc}",
            bar_format="{l_bar}{bar:30}{r_bar}",
            colour="green",
            leave=True,
        )

    def read(self, size=-1):
        data = self.f.read(size)
        if data:
            self.pbar.update(len(data))
        return data

    def seek(self, *args, **kwargs):
        return self.f.seek(*args, **kwargs)

    def tell(self):
        return self.f.tell()

    def close(self):
        self.pbar.close()
        self.f.close()

    def __iter__(self):
        return self

    def __next__(self):
        data = self.f.read(8192)
        if not data:
            self.pbar.close()
            raise StopIteration
        self.pbar.update(len(data))
        return data

    def __len__(self):
        return self.size


# ── Animated spinner ────────────────────────────────────────────────────────
class Spinner:
    """Animated spinner shown while a blocking network op runs.

    Usage:
        with Spinner("Mencari server . . ."):
            resp = requests.get(...)
        # or
        sp = Spinner("Memvalidasi . . .").start()
        ...
        sp.stop(f"{GREEN}[✔]{RESET} Selesai!")
    """

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message="", stream=sys.stdout):
        self.message = message
        self.stream = stream
        self._stop = threading.Event()
        self._thread = None
        self._start = 0.0

    def start(self, message=None):
        if message:
            self.message = message
        self._stop.clear()
        self._start = time.time()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def _spin(self):
        i = 0
        while not self._stop.is_set():
            elapsed = time.time() - self._start
            frame = self.FRAMES[i % len(self.FRAMES)]
            self.stream.write(f"\r\033[K{MAGENTA}{frame}{RESET} {self.message} {DIM}({elapsed:.0f}s){RESET}")
            self.stream.flush()
            i += 1
            time.sleep(0.1)

    def stop(self, final=None):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=0.5)
        self.stream.write("\r\033[K")
        self.stream.flush()
        if final:
            print(final)

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()


# ── Tab completion for file paths ───────────────────────────────────────────
def path_completer(text, state):
    """Enable TAB completion for file/directory paths in input()."""
    # Use the word readline passes us; fall back to the line buffer.
    line = text or readline.get_line_buffer() or "."
    expand = os.path.expanduser(line)
    dirname = os.path.dirname(expand) or "."
    basename = os.path.basename(expand)
    try:
        matches = glob.glob(os.path.join(dirname, basename + "*"))
    except Exception:
        matches = []
    results = []
    for m in matches:
        if os.path.isdir(m):
            results.append(m + "/")
        else:
            results.append(m)
    if state < len(results):
        return results[state]
    return None


def get_file_path():
    """Prompt for a file path with TAB completion enabled."""
    readline.set_completer(path_completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")
    while True:
        file_path = input(f"{CYAN}[📁]{RESET} Ketik berkas (TAB untuk auto-complete): ").strip()
        if not file_path:
            print(f"{RED}[❌]{RESET} Path tidak boleh kosong.")
            continue
        abs_path = os.path.abspath(os.path.expanduser(file_path))
        if os.path.isfile(abs_path):
            readline.set_completer(None)
            return abs_path
        print(f"{RED}[❌]{RESET} Berkas tidak ditemukan: {abs_path}")


# ── Utility ─────────────────────────────────────────────────────────────────
def fmt_size(nbytes):
    """Human-readable file size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} PB"


def get_file_info(filepath):
    """Return filename and size string."""
    name = os.path.basename(filepath)
    size = fmt_size(os.path.getsize(filepath))
    return name, size


# ── Upload services ─────────────────────────────────────────────────────────

def upload_pixeldrain(api_key, file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke Pixeldrain.com . . .")

    # Validate API key
    try:
        encoded = base64.b64encode(f":{api_key}".encode()).decode()
        with Spinner("Memvalidasi API key . . ."):
            resp = requests.get(
                "https://pixeldrain.com/api/user/files",
                headers={"Authorization": f"Basic {encoded}"},
                timeout=15,
            )
        if resp.status_code != 200:
            print(f"{RED}[❌]{RESET} Kunci API tidak valid! (HTTP {resp.status_code})\n")
            return
        print(f"{GREEN}[🔑]{RESET} API key valid ✓\n")
    except requests.RequestException as e:
        print(f"{RED}[❌]{RESET} Gagal memeriksa API: {e}\n")
        return

    # Upload with progress
    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                "https://pixeldrain.com/api/file",
                auth=("", api_key),
                files={"file": (name, reader)},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        file_id = resp.json().get("id")
        if file_id:
            print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
            print(f"{CYAN}[🔗]{RESET} https://pixeldrain.com/u/{file_id}\n")
        else:
            print(f"\n{RED}[❌]{RESET} Gagal mengunggah.\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")


def upload_gofile(file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke Gofile.io . . .")

    try:
        with Spinner("Mencari server Gofile . . ."):
            resp = requests.get("https://api.gofile.io/servers", timeout=15)
        resp.raise_for_status()
        server = resp.json()["data"]["servers"][0]["name"]
        print(f"{GREEN}[📡]{RESET} Server: {BOLD}{server}.gofile.io{RESET}\n")
    except (requests.RequestException, KeyError, IndexError) as e:
        print(f"{RED}[❌]{RESET} Gagal mendapatkan server: {e}\n")
        return

    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={"file": (name, reader)},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        link = resp.json()["data"]["downloadPage"]
        print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
        print(f"{CYAN}[🔗]{RESET} {link}\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")


def upload_bashupload(file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke Bashupload.app . . .")
    print(f"{CYAN}[🛈]{RESET} File disimpan 3 hari, hanya bisa diunduh sekali.\n")

    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                "https://bashupload.app",
                files={"file": (name, reader)},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        text = resp.text
        # Response may contain http:// or https:// — search for domain directly
        start = text.find("bashupload.app/")
        if start != -1:
            end = text.find("\n", start)
            if end == -1:
                end = len(text)
            link = text[start:end].strip()
            # Ensure protocol prefix
            if not link.startswith("http"):
                link = "https://" + link
            print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
            print(f"{CYAN}[🔗]{RESET} {link}\n")
        else:
            print(f"\n{RED}[❌]{RESET} URL tidak ditemukan di respons.\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")


def upload_devuploads(api_key, file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke Devuploads.com . . .")

    url = "https://devuploads.com/api/upload/server"
    try:
        with Spinner("Memvalidasi API key . . ."):
            resp = requests.get(f"{url}?key={api_key}", timeout=15)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        sess_id = data.get("sess_id")
        server_url = data.get("result")
        if status != 200 or not sess_id or not server_url:
            print(f"{RED}[❌]{RESET} API tidak valid atau info server kosong.\n")
            return
        print(f"{GREEN}[🔑]{RESET} API key valid ✓\n")
    except requests.RequestException as e:
        print(f"{RED}[❌]{RESET} Gagal validasi API: {e}\n")
        return

    if os.path.getsize(file_path) == 0:
        print(f"{RED}[❌]{RESET} File 0 byte — Devuploads tidak mendukung.\n")
        return

    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                server_url,
                files={"file": (name, reader)},
                data={"sess_id": sess_id, "utype": "reg"},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        result = resp.json()
        if isinstance(result, list):
            result = result[0]
        file_code = result.get("file_code")
        if file_code and file_code != "undef":
            print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
            print(f"{CYAN}[🔗]{RESET} https://devuploads.com/{file_code}\n")
        else:
            print(f"\n{RED}[❌]{RESET} Gagal: {result.get('file_status', result)}\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")


def upload_tmpfiles(file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke TmpFiles.org . . .")

    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                "https://tmpfiles.org/api/v1/upload",
                files={"file": (name, reader)},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "success":
            link = data["data"]["url"]
            print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
            print(f"{CYAN}[🔗]{RESET} {link}\n")
        else:
            print(f"\n{RED}[❌]{RESET} Gagal: {data}\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")
    except (KeyError, ValueError) as e:
        print(f"\n{RED}[❌]{RESET} Gagal parse respons: {e}\n")


def upload_uguu(file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke Uguu.se . . .")

    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                "https://uguu.se/upload",
                files={"files[]": (name, reader)},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            url = data["files"][0]["url"]
            print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
            print(f"{CYAN}[🔗]{RESET} {url}\n")
        else:
            print(f"\n{RED}[❌]{RESET} Gagal: {data}\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")


def upload_0x0st(file_path):
    name, size = get_file_info(file_path)
    print(f"{YELLOW}[↑]{RESET} Mengunggah {BOLD}{name}{RESET} ({size}) ke 0x0.st . . .")

    try:
        with open(file_path, "rb") as f:
            reader = ProgressReader(f, file_path, name)
            resp = requests.post(
                "https://0x0.st",
                files={"file": (name, reader)},
                timeout=600,
            )
            reader.close()
        resp.raise_for_status()
        link = resp.text.strip()
        print(f"\n{GREEN}[✔️]{RESET} Berkas berhasil diunggah!")
        print(f"{CYAN}[🔗]{RESET} {link}\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunggah: {e}\n")


# ── Download with progress ──────────────────────────────────────────────────
def download_file(url, output=None):
    """Download a file from URL with progress bar."""
    # ── URL normalization for known services ────────────────────────
    # Pixeldrain: /u/ID → /api/file/ID (raw file, no /download suffix)
    pd_match = re.search(r"pixeldrain\.com/u/([A-Za-z0-9]+)", url)
    if pd_match:
        url = f"https://pixeldrain.com/api/file/{pd_match.group(1)}"

    # TmpFiles.org: /xxxx/filename → fetch page, extract dynamic /dl/TOKEN/ link
    tf_match = re.search(r"tmpfiles\.org/(\w+)/(.+)", url)
    if tf_match and "/dl/" not in url and "/api/" not in url:
        try:
            with Spinner("Mencari link unduhan TmpFiles . . ."):
                page_resp = requests.get(url, timeout=15)
            dl_link = re.search(r'href="(https://tmpfiles\.org/dl/[^"]+)"', page_resp.text)
            if dl_link:
                url = dl_link.group(1)
        except requests.RequestException:
            pass  # fall through with original URL

    if not output:
        # Try to get filename from URL
        output = os.path.basename(url.split("?")[0])
        if not output:
            output = "downloaded_file"

    print(f"{YELLOW}[↓]{RESET} Mengunduh dari {BOLD}{url}{RESET} . . .")

    try:
        resp = requests.get(url, stream=True, timeout=30, allow_redirects=True)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))

        # Check if response is HTML (not a file) — always check
        ctype = resp.headers.get("content-type", "")
        if "text/html" in ctype:
            print(f"{RED}[❌]{RESET} URL mengembalikan HTML, bukan file.\n")
            return

        pbar = tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"  Download",
            bar_format="{l_bar}{bar:30}{r_bar}",
            colour="cyan",
            leave=True,
        )

        with open(output, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        pbar.close()

        print(f"\n{GREEN}[✔️]{RESET} Berkas tersimpan: {BOLD}{output}{RESET} ({fmt_size(os.path.getsize(output))})\n")
    except requests.RequestException as e:
        print(f"\n{RED}[❌]{RESET} Gagal mengunduh: {e}\n")


# ── Service definitions ─────────────────────────────────────────────────────
SERVICES = {
    1: {"name": "Pixeldrain.com", "needs_api": True,  "fn": upload_pixeldrain,  "url": "https://pixeldrain.com"},
    2: {"name": "Gofile.io",       "needs_api": False, "fn": upload_gofile,     "url": "https://api.gofile.io/servers"},
    3: {"name": "Bashupload.app",  "needs_api": False, "fn": upload_bashupload, "url": "https://bashupload.app"},
    4: {"name": "Devuploads.com",  "needs_api": True,  "fn": upload_devuploads, "url": "https://devuploads.com"},
    5: {"name": "TmpFiles.org",     "needs_api": False, "fn": upload_tmpfiles,    "url": "https://tmpfiles.org"},
    6: {"name": "Uguu.se",         "needs_api": False, "fn": upload_uguu,       "url": "https://uguu.se"},
    7: {"name": "0x0.st",          "needs_api": False, "fn": upload_0x0st,      "url": "https://0x0.st"},
}


# ── Service health check ────────────────────────────────────────────────────
def check_all_services(timeout=8):
    """Ping semua service endpoint, return dict {sid: bool}."""
    results = {}

    def _check(sid, url):
        try:
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            # Some services don't support HEAD, fall back to GET
            if resp.status_code == 405:
                resp = requests.get(url, timeout=timeout, stream=True)
                resp.close()
            results[sid] = resp.status_code < 500
        except requests.RequestException:
            results[sid] = False

    threads = []
    for sid, info in SERVICES.items():
        t = threading.Thread(
            target=_check, args=(sid, info["url"]), daemon=True
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join(timeout + 2)

    return results


def print_service_status():
    """Print health check table for all services with spinner + summary."""
    print(f"\n  {BOLD}── Cek Status Server ──{RESET}\n")
    with Spinner("Menghubungi server . . ."):
        results = check_all_services()
    online = sum(1 for v in results.values() if v)
    total = len(results)
    for sid, info in SERVICES.items():
        up = results.get(sid, False)
        status = f"{GREEN}● ONLINE {RESET}" if up else f"{RED}● OFFLINE{RESET}"
        api_tag = f"{YELLOW}(API){RESET}" if info["needs_api"] else "       "
        print(f"  {status}  {CYAN}{sid}.{RESET} {info['name']:<18s} {api_tag}")
    if online == total:
        summary = f"{GREEN}✓ {online}/{total} server online{RESET}"
    else:
        summary = f"{YELLOW}⚠ {online}/{total} online · {total - online} offline{RESET}"
    print(f"\n  {summary}\n")


# ── ASCII art ───────────────────────────────────────────────────────────────
def print_banner():
    print(f"""{GREEN}
  ╔═══════════════════════════════════════════════╗
  ║          ╦  ╦╔═╗╦ ╦╔═╗╔═╗╦ ╦╔═╗╦═╗           ║
  ║          ║  ║║╣ ╠═╣╠═╣║   ╠═╣║╣ ╠╦╝           ║
  ║          ╩═╝╚╚═╝╩ ╩╩ ╩╚═╝ ╩ ╩╚═╝╩╚═           ║
  ║                                               ║
  ║  v2.2  ·  Multi-platform File Uploader        ║
  ║         by officialputuid                     ║
  ╚═══════════════════════════════════════════════╝{RESET}
""")


def print_service_art(service_id):
    """Print compact ASCII art for the selected service."""
    arts = {
        1: f"{GREEN}  ┃ Pixeldrain{RESET}",
        2: f"{GREEN}  ┃ Gofile.io{RESET}",
        3: f"{GREEN}  ┃ Bashupload{RESET}",
        4: f"{GREEN}  ┃ Devuploads{RESET}",
        5: f"{GREEN}  ┃ TmpFiles.org{RESET}",
        6: f"{GREEN}  ┃ Uguu.se{RESET}",
        7: f"{GREEN}  ┃ 0x0.st{RESET}",
    }
    print(arts.get(service_id, ""))
    print(f"  {'─' * 43}\n")


# ── Interactive mode ────────────────────────────────────────────────────────
def interactive_mode():
    print_banner()
    print_service_status()

    while True:
        print(f"\n{BOLD}  🚀 Pilih layanan:{RESET}")
        for sid, info in SERVICES.items():
            api_tag = f"{YELLOW}(API){RESET}" if info["needs_api"] else ""
            print(f"  {CYAN}{sid}.{RESET} {info['name']} {api_tag}")
        print(f"  {CYAN}8.{RESET} Download File")
        print(f"  {CYAN}0.{RESET} Keluar\n")

        try:
            choice = input(f"{CYAN}[❓]{RESET} Pilihan: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{GREEN}[✔️]{RESET} Program ditutup!\n")
            sys.exit(0)

        if choice == "0":
            print(f"{GREEN}[✔️]{RESET} Terimakasih telah menggunakan UploadGen!\n")
            break

        if choice == "8":
            # Download mode
            url = input(f"{CYAN}[🔗]{RESET} URL file: ").strip()
            if not url:
                print(f"{RED}[❌]{RESET} URL tidak boleh kosong.\n")
                continue
            output = input(f"{CYAN}[💾]{RESET} Nama file output (kosong=auto): ").strip() or None
            download_file(url, output)
        elif choice in ("1", "2", "3", "4", "5", "6", "7"):
            sid = int(choice)
            info = SERVICES[sid]
            print_service_art(sid)
            print(f"{CYAN}[🛈]{RESET} Layanan: {BOLD}{info['name']}{RESET}\n")

            if info["needs_api"]:
                while True:
                    api_key = input(f"{CYAN}[🔑]{RESET} API Key: ").strip()
                    if api_key:
                        break
                    print(f"{RED}[❌]{RESET} API Key tidak boleh kosong.\n")

            file_path = get_file_path()

            if info["needs_api"]:
                info["fn"](api_key, file_path)
            else:
                info["fn"](file_path)
        else:
            print(f"{RED}[❌]{RESET} Pilihan tidak valid.\n")
            continue

        # Ask to repeat
        repeat = input(f"{CYAN}[🔄]{RESET} Lagi? (y/n): ").strip().lower()
        if repeat != "y":
            print(f"\n{GREEN}[✔️]{RESET} Terimakasih telah menggunakan UploadGen!\n")
            break
        print()


# ── CLI entry ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="UploadGen v2.2 — Unggah/unduh berkas ke berbagai layanan.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-s", "--service", type=int, choices=[1, 2, 3, 4, 5, 6, 7],
        help="Pilih layanan upload:\n"
             "  1=Pixeldrain  2=Gofile  3=Bashupload\n"
             "  4=Devuploads  5=TmpFiles 6=Uguu\n"
             "  7=0x0.st",
    )
    parser.add_argument("-f", "--file", help="Path berkas yang akan diunggah")
    parser.add_argument("-d", "--download", help="URL untuk diunduh")
    parser.add_argument("-o", "--output", help="Nama file output untuk download")
    parser.add_argument("--check", action="store_true", help="Cek status semua server (online/offline)")

    args = parser.parse_args()

    # Health check mode
    if args.check:
        print_banner()
        print_service_status()
        return

    # Download mode
    if args.download:
        download_file(args.download, args.output)
        return

    # Upload mode via CLI args
    if args.service and args.file:
        abs_path = os.path.abspath(os.path.expanduser(args.file))
        if not os.path.isfile(abs_path):
            print(f"\n{RED}[❌]{RESET} Berkas tidak ditemukan: {abs_path}\n")
            sys.exit(1)

        print_banner()
        print_service_status()
        print_service_art(args.service)
        info = SERVICES[args.service]
        print(f"{CYAN}[🛈]{RESET} Layanan: {info['name']}\n")

        if info["needs_api"]:
            api_key = input(f"{CYAN}[🔑]{RESET} API Key: ").strip()
            info["fn"](api_key, abs_path)
        else:
            info["fn"](abs_path)
        return

    # Interactive mode
    interactive_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}[✔️]{RESET} Program ditutup!\n")
        sys.exit(0)
