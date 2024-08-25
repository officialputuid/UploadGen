# Copyright (C) 2024 officialputuid

import os
import sys
import argparse
import requests
import base64

def upload_pixeldrain(api_key, file_path):
    print(f"[⌛] Mengunggah {file_path} ke Pixeldrain.com . . .")

    # Validasi kunci API menggunakan metode yang diadaptasi
    try:
        # Encode kunci API ke Base64
        encoded_api_key = base64.b64encode(f":{api_key}".encode()).decode()

        # Gunakan header Authorization dengan kunci yang ter-encode
        check_api_response = requests.get(
            "https://pixeldrain.com/api/user/files",
            headers={
                "Authorization": f"Basic {encoded_api_key}"
            }
        )
        if check_api_response.status_code == 200:
            print("[✔️] Kunci API Pixeldrain valid!")
        else:
            print(f"[❌] Kunci API Pixeldrain tidak valid! Kode status: {check_api_response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"[❌] Gagal memeriksa kunci API: {e}\n")
        return

    # Lanjutkan dengan mengunggah file
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://pixeldrain.com/api/file",
                auth=('', api_key),
                files={'file': f},
            )
        response.raise_for_status()
        response_json = response.json()
        file_id = response_json.get('id')
        if file_id:
            print("[✔️] Berkas berhasil diunggah!")
            print(f"[🔗] URL berkas Anda: https://pixeldrain.com/u/{file_id}\n")
        else:
            print("[❌] Gagal mengunggah.")
    except requests.exceptions.SSLError as ssl_err:
        print(f"[❌] Gagal mengunggah berkas: Masalah SSL. Pesan kesalahan: {ssl_err}\n")
    except requests.exceptions.RequestException as e:
        print(f"[❌] Gagal mengunggah berkas: {e}\n")
    except requests.exceptions.JSONDecodeError:
        print("[❌] Tidak dapat menguraikan respons sebagai JSON.\n")
    except Exception as e:
        print(f"[❌] Terjadi kesalahan yang tidak diketahui: {e}\n")
        sys.exit(1)

def upload_gofile(file_path):
    print(f"[⌛] Mengunggah {file_path} ke Gofile.io . . .")
    try:
        server_response = requests.get("https://api.gofile.io/servers")
        server_response.raise_for_status()
        server = server_response.json()['data']['servers'][0]['name']
    except requests.RequestException as e:
        print(f"[❌] Gagal mendapatkan informasi server: {e}\n")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={'file': f}
            )
            upload_response.raise_for_status()
        link = upload_response.json()['data']['downloadPage']
        print("[✔️] Berkas berhasil diunggah!")
        print(f"[🔗] URL berkas Anda: {link}\n")
    except requests.RequestException as e:
        print(f"[❌] Gagal mengunggah berkas: {e}\n")
        sys.exit(1)

def upload_bashupload(file_path):
    print(f"[⌛] Mengunggah {file_path} ke Bashupload.com . . .")
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://bashupload.com",
                files={'file': f}
            )
        response.raise_for_status()
        # Ekstrak URL dari respons
        response_text = response.text
        url_start = response_text.find("https://bashupload.com/")
        if url_start != -1:
            url_end = response_text.find("\n", url_start)
            if url_end == -1:
                url_end = len(response_text)
            link = response_text[url_start:url_end].strip()
            print("[✔️] Berkas berhasil diunggah!")
            print(f"[🔗] URL berkas Anda: {link}\n")
        else:
            print("[❌] Gagal mengunggah berkas. URL tidak ditemukan.\n")
    except requests.RequestException as e:
        print(f"[❌] Gagal mengunggah berkas: {e}\n")
        sys.exit(1)

def upload_devuploads(api_key, file_path):
    print(f"[⌛] Mengunggah {file_path} ke Devuploads.com . . .")
    url = "https://devuploads.com/api/upload/server"

    try:
        # Validasi kunci API
        check_response = requests.get(f"{url}?key={api_key}")
        check_response.raise_for_status()
        res_json = check_response.json()

        res_status = res_json.get("status")
        sess_id = res_json.get("sess_id")
        server_url = res_json.get("result")

        if res_status == 200:
            print("[✔️] Kunci API Devuploads valid!")
            if not sess_id or not server_url:
                print(f"[❌] Informasi server tidak tersedia. Kunci API valid tetapi informasi server kosong.")
                return
        else:
            print(f"[❌] Kunci API Devuploads tidak valid! Kode status: {res_status}")
            return

        # Periksa ukuran file
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"[❌] File {file_path} tidak memiliki isi apapun.\n[❌] Devuploads tidak dapat mengunggah berkas dengan ukuran 0 byte")
            return

        # Lanjutkan dengan mengunggah file
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                server_url,
                files={"file": f},
                data={"sess_id": sess_id, "utype": "reg"},
            )
        upload_response.raise_for_status()

        upload_response_json = upload_response.json()

        if isinstance(upload_response_json, list):
            upload_response_json = upload_response_json[0]

        file_code = upload_response_json.get("file_code")
        file_status = upload_response_json.get("file_status")

        if file_code == 'undef':
            print(f"[❌] Gagal mengunggah: {file_status}\n")
        elif file_code:
            print("[✔️] Berkas berhasil diunggah!")
            print(f"[🔗] URL berkas Anda: https://devuploads.com/{file_code}\n")
        else:
            print(f"[❌] Gagal mengunggah: {upload_response_json}\n")

    except requests.RequestException as e:
        print(f"[❌] Gagal mengunggah berkas: {e}\n")
        sys.exit(1)

def upload_fileio(file_path):
    print(f"[⌛] Uploading {file_path} to File.io . . .")
    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                'https://file.io',
                files={'file': f}
            )
            upload_response.raise_for_status()
        link = upload_response.json()['link']
        print("[✔️] File successfully uploaded!")
        print(f"[🔗] Your file URL: {link}\n")
    except requests.RequestException as e:
        print(f"[❌] Failed to upload file: {e}\n")
        sys.exit(1)

# ASCII art
pixeldrain_art = "\033[92m" + r"""
 ____  _          _     _           _                            
|  _ \(_)_  _____| | __| |_ __ __ _(_)_ __    ___ ___  _ __ ___  
| |_) | \ \/ / _ \ |/ _` | '__/ _` | | '_ \  / __/ _ \| '_ ` _ \ 
|  __/| |>  <  __/ | (_| | | | (_| | | | | || (_| (_) | | | | | |
|_|   |_/_/\_\___|_|\__,_|_|  \__,_|_|_| |_(_)___\___/|_| |_| |_|
""" + "\033[0m"

gofile_art = "\033[92m" + r"""
  ____        __ _ _        _       
 / ___| ___  / _(_) | ___  (_) ___  
| |  _ / _ \| |_| | |/ _ \ | |/ _ \ 
| |_| | (_) |  _| | |  __/_| | (_) |
 \____|\___/|_| |_|_|\___(_)_|\___/ 
""" + "\033[0m"

bashupload_art = "\033[92m" + r"""
 ____            _                 _                 _                      
| __ )  __ _ ___| |__  _   _ _ __ | | ___   __ _  __| |  ___ ___  _ __ ___  
|  _ \ / _` / __| '_ \| | | | '_ \| |/ _ \ / _` |/ _` | / __/ _ \| '_ ` _ \ 
| |_) | (_| \__ \ | | | |_| | |_) | | (_) | (_| | (_| || (_| (_) | | | | | |
|____/ \__,_|___/_| |_|\__,_| .__/|_|\___/ \__,_|\__,_(_)___\___/|_| |_| |_|
                            |_|                                              
""" + "\033[0m"

devuploads_art = "\033[92m" + r"""
 ____                         _                 _                          
|  _ \  _____   ___   _ _ __ | | ___   __ _  __| |___   ___ ___  _ __ ___  
| | | |/ _ \ \ / / | | | '_ \| |/ _ \ / _` |/ _` / __| / __/ _ \| '_ ` _ \ 
| |_| |  __/\ V /| |_| | |_) | | (_) | (_| | (_| \__ \| (_| (_) | | | | | |
|____/ \___| \_/  \__,_| .__/|_|\___/ \__,_|\__,_|___(_)___\___/|_| |_| |_|
                       |_|                                                 
""" + "\033[0m"

file_art = "\033[92m" + r"""
 _____ _ _        _       
|  ___(_) | ___  (_) ___  
| |_  | | |/ _ \ | |/ _ \ 
|  _| | | |  __/_| | (_) |
|_|   |_|_|\___(_)_|\___/ 
""" + "\033[0m"

def print_ascii_art(service):
    if service == 1:
        print(pixeldrain_art)
    elif service == 2:
        print(gofile_art)
    elif service == 3:
        print(bashupload_art)
    elif service == 4:
        print(devuploads_art)
    elif service == 5:
        print(file_art)

def interactive_mode():
    print("\033[92m" + r"""
 _   _       _                 _  ____            
| | | |_ __ | | ___   __ _  __| |/ ___| ___ _ __  
| | | | '_ \| |/ _ \ / _` |/ _` | |  _ / _ \ '_ \ 
| |_| | |_) | | (_) | (_| | (_| | |_| |  __/ | | |
 \___/| .__/|_|\___/ \__,_|\__,_|\____|\___|_| |_|
      |_|                                         

Versi: v1.5
oleh officialputuid   
    """ + "\033[0m")

    while True:
        print("Pilih layanan untuk mengunggah:")
        print("1. Pixeldrain.com (Memerlukan API)")
        print("2. GoFile.io")
        print("3. Bashupload.com (Sementara)")
        print("4. Devuploads.com (Memerlukan API)")
        print("5. File.io")

        try:
            choice = input("\n[❓] Masukkan nomor pilihan Anda: ")

            # ASCII
            print_ascii_art(int(choice))

            if choice == '1':
                while True:
                    print("\n[🛈] Anda memilih:\n[1] Pixeldrain.com (Memerlukan API)\n")
                    api_key = input("[🔑] Masukkan kunci API Pixeldrain Anda: ").strip()
                    if api_key:
                        break
                    print("[❌] Kunci API tidak boleh kosong. Silakan masukkan kunci API yang benar.")
                upload_pixeldrain(api_key, get_file_path())
            elif choice == '2':
                print("[🛈] Anda memilih:\n[2] GoFile.io\n")
                upload_gofile(get_file_path())
            elif choice == '3':
                print("[🛈] Anda memilih:\n[3] Bashupload.com\n[🛈] File disimpan selama 3 hari dan hanya bisa diunduh sekali.\n")
                upload_bashupload(get_file_path())
            elif choice == '4':
                while True:
                    print("\n[🛈] Anda memilih:\n[4] Devuploads.com (Memerlukan API)\n[🛈] Devuploads tidak dapat mengunggah berkas dengan ukuran 0 byte\n")
                    api_key = input("[🔑] Masukkan kunci API Devuploads Anda: ").strip()
                    if api_key:
                        break
                    print("[❌] Kunci API tidak boleh kosong. Silakan masukkan kunci API yang benar.")
                upload_devuploads(api_key, get_file_path())
            elif choice == '5':
                print("[🛈] Anda memilih:\n[5] File.io\n")
                upload_fileio(get_file_path())
            else:
                print("[❌] Pilihan tidak valid.")
                sys.exit(1)

            # Tanyakan pengguna apakah ingin mengunggah file lain
            repeat = input("[🔄] Ingin mengunggah file lain? (y/n): ").strip().lower()
            if repeat == 'n':
                print("[✔️] Terimakasih telah menggunakan UploadGen!\n")
                break

        except KeyboardInterrupt:
            print("\n[✔️] Program telah ditutup!\n")
            sys.exit(0)

def get_file_path():
    while True:
        file_path = input("[📁] Ketik berkas yang akan diunggah: ").strip()
        if file_path and os.path.isfile(os.path.abspath(file_path)):
            return os.path.abspath(file_path)
        print("[❌] Berkas tidak ditemukan! Harap masukkan berkas yang valid.")

def main():
    parser = argparse.ArgumentParser(description="Unggah berkas ke berbagai layanan berbagi berkas.")
    parser.add_argument("-s", "--service", type=int, choices=[1, 2, 3, 4, 5],
                        help="Pilih layanan: 1=Pixeldrain, 2=GoFile, 3=Bashupload, 4=Devuploads 5=File")
    parser.add_argument("-f", "--file", help="Path berkas yang akan diunggah")

    args = parser.parse_args()

    if args.service and args.file:
        if not os.path.isfile(os.path.abspath(args.file)):
            print("\n[❌] Berkas tidak ditemukan!\n")
            sys.exit(1)

        file_path = os.path.abspath(args.file)

        # ASCII
        print_ascii_art(args.service)

        if args.service == 1:
            print("\n[🛈] Anda memilih: [1] Pixeldrain.com (Memerlukan API)\n")
            api_key = input("[🔑] Masukkan kunci API Pixeldrain Anda: ").strip()
            upload_pixeldrain(api_key, file_path)
        elif args.service == 2:
            print("\n[🛈] Anda memilih: [2] GoFile.io\n")
            upload_gofile(file_path)
        elif args.service == 3:
            print("\n[🛈] Anda memilih: [3] Bashupload.com\n[🛈] File disimpan selama 3 hari dan hanya bisa diunduh sekali.\n")
            upload_bashupload(file_path)
        elif args.service == 4:
            print("\n[🛈] Anda memilih: [4] Devuploads.com (Memerlukan API)\n[🛈] Devuploads tidak dapat mengunggah berkas dengan ukuran 0 byte\n")
            api_key = input("[🔑] Masukkan kunci API Devuploads Anda: ").strip()
            upload_devuploads(api_key, file_path)
        elif args.service == 5:
            print("\n[🛈] Anda memilih: [5] File.io\n")
            upload_fileio(file_path)
    else:
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[✔️] Program sudah ditutup!\n")
        sys.exit(0)
