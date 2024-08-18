import os
import sys
import requests

def upload_pixeldrain(api_key, file_path):
    print(f"[⌛] Ngunggahang {file_path} ka Pixeldrain.com . . .")
    with open(file_path, 'rb') as f:
        response = requests.post(
            "https://pixeldrain.com/api/file",
            auth=('', api_key),
            files={'file': f},
        )
    try:
        response_json = response.json()
        file_id = response_json.get('id')
        if file_id:
            print("[✔️] Berkas puniki sampun prasida kaunggahang!")
            print(f"[🔗] URL berkas ragane: https://pixeldrain.com/u/{file_id}")
        else:
            print("[❌] Gagal ngunggahang.")
    except requests.exceptions.JSONDecodeError:
        print("[❌] Nénten prasida nlatarang pasaut dados JSON.")
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
        print(f"[❌] Nénten prasida ngunggahang berkas: {e}")
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
        print(f"[❌] Nénten prasida ngunggahang berkas: {e}")
        sys.exit(1)

def main():
    print("\033[92m" + """
UploadGen v1.1
olih officialputuid   
    """ + "\033[0m")

    while True:
        print("Pilih UploadGen antuk:")
        print("1. Pixeldrain.com (Nyaratang API)")
        print("2. GoFile.io")
        print("3. Bashupload.com (Wantah dados kaanggén/kaunduh apisan)")

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
                print("[🛈] Ragane sampun milih:\n[3] Bashupload.com\n[🛈] Wantah dados kaanggén/kaunduh apisan\n")
                api_key = None
            else:
                print("[❌] Pilihan sané nenten valid.")
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

            # Ask user if they want to upload another file
            repeat = input("\n[🔄] Ingin ngunggahang berkas malih? (y/n): ").strip().lower()
            if repeat != 'y':
                print("\n[✔️] Program sampun katutup!")
                break

        except KeyboardInterrupt:
            print("\n[✔️] Program sampun katutup!")
            sys.exit(0)

if __name__ == "__main__":
    main()
