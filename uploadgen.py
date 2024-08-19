# Copyright (C) 2024 officialputuid

import os
import sys
import requests
import base64

def upload_pixeldrain(api_key, file_path):
    print(f"[⌛] Ngunggahang {file_path} ka Pixeldrain.com . . .")

    # Validate API key using the adapted method
    try:
        # Encode the API key to Base64
        encoded_api_key = base64.b64encode(f":{api_key}".encode()).decode()

        # Use the Authorization header with the encoded key
        check_api_response = requests.get(
            "https://pixeldrain.com/api/user/files",
            headers={
                "Authorization": f"Basic {encoded_api_key}"
            }
        )
        if check_api_response.status_code == 200:
            print("[✔️] Kunci API Pixeldrain valid!")
        else:
            print(f"[❌] Kunci API Pixeldrain nenten valid! Kode status: {check_api_response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"[❌] Gagal antuk mariksa kunci API: {e}")
        return

    # Proceed with file upload
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
            print("[✔️] Berkas puniki sampun prasida kaunggahang!")
            print(f"[🔗] URL berkas ragane: https://pixeldrain.com/u/{file_id}")
        else:
            print("[❌] Gagal ngunggahang.")
    except requests.exceptions.SSLError as ssl_err:
        print(f"[❌] Gagal ngunggahang berkas: Masalah SSL. Pesan kesalahan: {ssl_err}")
    except requests.exceptions.RequestException as e:
        print(f"[❌] Gagal ngunggahang berkas: {e}")
    except requests.exceptions.JSONDecodeError:
        print("[❌] Nenten prasida nlatarang pasaut dados JSON.")
    except Exception as e:
        print(f"[❌] Wénten kaiwangan sané nénten katenger: {e}")
        sys.exit(1)

def upload_gofile(file_path):
    print(f"[⌛] Ngunggahang {file_path} ka Gofile.io . . .")
    try:
        server_response = requests.get("https://api.gofile.io/servers")
        server_response.raise_for_status()
        server = server_response.json()['data']['servers'][0]['name']
    except requests.RequestException as e:
        print(f"[❌] Gagal antuk ngamolihang informasi server: {e}")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={'file': f}
            )
            upload_response.raise_for_status()
        link = upload_response.json()['data']['downloadPage']
        print("[✔️] Berkas puniki sampun prasida kaunggahang!")
        print(f"[🔗] URL berkas ragane: {link}")
    except requests.RequestException as e:
        print(f"[❌] Nenten prasida ngunggahang berkas: {e}")
        sys.exit(1)

def upload_bashupload(file_path):
    print(f"[⌛] Ngunggahang {file_path} ka Bashupload.com . . .")
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://bashupload.com",
                files={'file': f}
            )
        response.raise_for_status()
        # Extract URL from response
        response_text = response.text
        url_start = response_text.find("https://bashupload.com/")
        if url_start != -1:
            url_end = response_text.find("\n", url_start)
            if url_end == -1:
                url_end = len(response_text)
            link = response_text[url_start:url_end].strip()
            print("[✔️] Berkas puniki sampun prasida kaunggahang!")
            print(f"[🔗] URL berkas ragane: {link}")
        else:
            print("[❌] Gagal ngunggahang berkas. URL nenten kapanggihin.")
    except requests.RequestException as e:
        print(f"[❌] Nenten prasida ngunggahang berkas: {e}")
        sys.exit(1)

def upload_devuploads(api_key, file_path):
    print(f"[⌛] Ngunggahang {file_path} ka Devuploads.com . . .")
    url = "https://devuploads.com/api/upload/server"

    try:
        # Validate API key
        check_response = requests.get(f"{url}?key={api_key}")
        check_response.raise_for_status()
        res_json = check_response.json()

        res_status = res_json.get("status")
        sess_id = res_json.get("sess_id")
        server_url = res_json.get("result")

        if res_status == 200:
            print("[✔️] Kunci API Devuploads valid!")
            if not sess_id or not server_url:
                print(f"[❌] Informasi server nenten prasida. Kunci API valid tapi server informasi kosong.")
                return
        else:
            print(f"[❌] Kunci API Devuploads nenten valid! Kode status: {res_status}")
            return

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"[❌] File {file_path} nenten madaging informasi napi-napi.\n[❌] Devuploads nenten prasida ngunggahang berkas nganggen 0 bytes")
            return

        # Proceed with file upload
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
            print(f"[❌] Gagal ngunggahang: {file_status}")
        elif file_code:
            print("[✔️] Berkas puniki sampun prasida kaunggahang!")
            print(f"[🔗] URL berkas ragane: https://devuploads.com/{file_code}")
        else:
            print(f"[❌] Gagal ngunggahang: {upload_response_json}")

    except requests.RequestException as e:
        print(f"[❌] Nenten prasida ngunggahang berkas: {e}")
        sys.exit(1)

def main():
    print("\033[92m" + """
UploadGen v1.3
olih officialputuid   
    """ + "\033[0m")

    while True:
        print("Pilih UploadGen antuk:")
        print("1. Pixeldrain.com (Nyaratang API)")
        print("2. GoFile.io")
        print("3. Bashupload.com (Wantah dados kaanggen/kaunduh apisan)")
        print("4. Devuploads.com (Nyaratang API)")

        try:
            choice = input("\n[❓] Ketik nomor sane pilih ragane: ")

            if choice == '1':
                while True:
                    print("\n[🛈] Ragane sampun milih:\n[1] Pixeldrain.com (Nyaratang API)\n")
                    api_key = input("[🔑] Ketik kunci API Pixeldrain ragane: ").strip()
                    if api_key:
                        break
                    print("[❌] Kunci API nenten dados kosong. Indayang ngranjingang kunci API sane patut.")
            elif choice == '2':
                print("[🛈] Ragane sampun milih:\n[2] GoFile.io\n")
                api_key = None
            elif choice == '3':
                print("[🛈] Ragane sampun milih:\n[3] Bashupload.com\n[🛈] Wantah dados kaanggen/kaunduh apisan\n")
                api_key = None
            elif choice == '4':
                while True:
                    print("\n[🛈] Ragane sampun milih:\n[4] Devuploads.com (Nyaratang API)\n[🛈] Devuploads nenten prasida ngunggahang berkas nganggen 0 byte\n")
                    api_key = input("[🔑] Ketik kunci API Devuploads ragane: ").strip()
                    if api_key:
                        break
                    print("[❌] Kunci API nenten dados kosong. Indayang ngranjingang kunci API sane patut.")
            else:
                print("[❌] Pilihan sane nenten valid.")
                sys.exit(1)

            while True:
                file_path = input("[📁] Ketik berkas sane jagi kaunggahang: ").strip()
                if file_path and os.path.isfile(os.path.abspath(file_path)):
                    break
                print("[❌] Berkas nenten katemu! Indayang ngranjingang berkas sane patut.")

            file_path = os.path.abspath(file_path)

            if choice == '1':
                upload_pixeldrain(api_key, file_path)
            elif choice == '2':
                upload_gofile(file_path)
            elif choice == '3':
                upload_bashupload(file_path)
            elif choice == '4':
                upload_devuploads(api_key, file_path)

            # Ask user if they want to upload another file
            while True:
                repeat = input("\n[🔄] Ingin ngunggahang berkas malih? (y/n): ").strip().lower()
                if repeat in ['y', 'n']:
                    break
                print("[❌] Pilihan nenten valid. Mangda milih 'y' utawi 'n'.")

            if repeat == 'n':
                print("[✔️] Program sampun katutup!")
                break

        except KeyboardInterrupt:
            print("\n[✔️] Program sampun katutup!")
            sys.exit(0)

if __name__ == "__main__":
    main()
