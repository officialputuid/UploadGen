# UploadGen

`UploadGen` inggih punika skrip Python sane kakaryanin mangda dangan ngunggahang berkas ring platform berbagi berkas sane kasub. Utilitas puniki ngawentenang sederhana ngunggahang berkas antuk ngicenin antarmuka baris perintah sane lurus.

## Pitur

- **Unggah ka PixelDrain**: Merluang kunci API anggén otentikasi.
- **Unggah ka GoFile**: Otomatis milih server sané jagi kaunggahang.
- **Unggah ka Bashupload**: Berkas kasimpen 3 rahina lan prasida kaunduh wantah apisan.
- **Unggah ka Devuploads**: Merluang kunci API anggén otentikasi.

## Sarat

- Python 3.x
- Perpustakaan `requests` (dados kapasang saking `pip`)

## Pamasangan

1. Kloning repositori utawi ngunduh file naskah.

   ```bash
   git clone https://github.com/officialputuid/UploadGen.git
   cd UploadGen
   ```

2. Instal perpustakaan Python sane kabuatang:

   ```bash
   pip install requests
   ```

## Pangangge

1. **Jalasang Naskah**

   ```bash
   python uploadgen.py
   ```

2. **Pilih Layanan Unggah**

   Risampuné ngawitin skrip, Sameton pacang katunasin milih layanan unggah:

   - **1**: Unggahang ka PixelDrain (kaperluang kunci API)
   - **2**: Unggahang ka GoFile (nénten perlu kunci API)
   - **3**: Unggahang ka Bashupload (Wantah dados kaanggen/kaunduh apisan)
   - **4**: Unggahang ka Devuploads (kaperluang kunci API)

3. **Ngicenin Gatra sane Kaperluang**

   - Antuk PixelDrain: Unggahang kunci API Sameton yéning katunasin.
   - Antuk GoFile: Nénten perlu kunci API.
   - Antuk Bashupload: Nénten perlu kunci API.
   - Antuk Devuploads: Unggahang kunci API Sameton yéning katunasin.

4. **Tentuang Jalur Berkas**

   Unggahang jalur ka berkas sané jagi kaunggahang. Skrip punika pacang ngevalidasi jalur berkas lan nglanturang antuk ngunggahang.

## Conto

```
UploadGen v1.0
by officialputuid

Ketik nomor sane pilih ragane:
1. Pixeldrain.com (Kaperluang API)
2. GoFile.io
3. Bashupload.com (Wantah dados kaanggén/kaunduh apisan)
4. Devuploads.com (Kaperluang API)

Unggahang nomer sané kapilih: 1
Ketik kunci API Pixeldrain ragane: kunci_api_sametoné
Ketik berkas sane jagi kaunggahang: /path/to/your/file.txt
Ngunggahang /path/to/your/file.txt ka PixelDrain.com
Kunci API Pixeldrain valid!
Berkas puniki sampun prasida kaunggahang!
URL berkas ragane:: https://pixeldrain.com/u/file

Unggahang nomer sané kapilih: 2
Ketik berkas sane jagi kaunggahang: /path/to/your/file.txt
Ngunggahang /path/to/your/file.txt ka GoFile.io
Berkas puniki sampun prasida kaunggahang!
URL berkas ragane: https://gofile.io/d/file

Unggahang nomer sané kapilih: 3
Ketik berkas sane jagi kaunggahang: /path/to/your/file.txt
Ngunggahang /path/to/your/file.txt ka Bashupload.com
Berkas puniki sampun prasida kaunggahang!
URL berkas ragane: https://bashupload.com/?/file

Unggahang nomer sané kapilih: 4
Ketik berkas sane jagi kaunggahang: /path/to/your/file.txt
Ngunggahang /path/to/your/file.txt ka Devuploads.com
Kunci API Devuploads valid!
Berkas puniki sampun prasida kaunggahang!
URL berkas ragane: https://devuploads.com/file
```

## Penanganan Kaiwangan

- **Pikobet Kunci API**: Pastikayang Sameton ngicénin kunci API sané patut anggén PixelDrain lan Devuploads.
- **Masalah Jalur Berkas**: Pastikayang jalur berkas sampun patut lan berkas punika wenten.

## Makontribusi

Bebas ngirimang pikobet utawi pinunas tarik mangda prasida nincapang naskah. Pastikayang pauwahan Sametoné sampun kauji becik sadurung kakirim.

## Lisensi

Proyek puniki polih lisensi ring sor Lisensi MIT - cingak berkas [LICENSE](LICENSE) antuk rinciannyané.

## Cingakin nganggén basa Inggris?

[README-EN](README-en.md)
