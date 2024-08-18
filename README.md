# UploadGen

`UploadGen` inggih punika skrip Python sane kakaryanin mangda dangan ngunggahang berkas ring platform berbagi berkas sane kasub: PixelDrain, GoFile lan Bashupload. Utilitas puniki ngawentenang sederhana ngunggahang berkas antuk ngicenin antarmuka baris perintah sane lurus.

## Pitur

- **Unggah ka PixelDrain**: Merluang kunci API anggén otentikasi.
- **Unggah ka GoFile**: Otomatis milih server sané jagi kaunggahang.
- **Unggah ka Bashupload**: Berkas kasimpen 3 rahina lan prasida kaunduh wantah apisan.

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
   - **3**: Unggahang ka Bashupload

3. **Ngicenin Gatra sane Kaperluang**

   - Antuk PixelDrain: Unggahang kunci API Sameton yéning katunasin.
   - Antuk GoFile: Nénten perlu kunci API.

4. **Tentuang Jalur Berkas**

   Unggahang jalur ka berkas sané jagi kaunggahang. Skrip punika pacang ngevalidasi jalur berkas lan nglanturang antuk ngunggahang.

## Conto

```
UploadGen v1.0
by officialputuid

Ketik nomor sane pilih ragane:
1. Pixeldrain.com (Kaperluang API)
2. GoFile.io
2. Bashupload.com (Wantah dados kaanggén/kaunduh apisan)

Unggahang nomer sané kapilih: 1
Ketik kunci API Pixeldrain ragane: kunci_api_sametoné
Ketik berkas sane jagi kaunggahang: /path/to/your/file.txt
Ngunggahang /path/to/your/file.txt ka PixelDrain.com
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
```

## Penanganan Kaiwangan

- **Pikobet Kunci API**: Pastikayang Sameton ngicénin kunci API sané patut anggén PixelDrain.
- **Masalah Jalur Berkas**: Pastikayang jalur berkas sampun patut lan berkas punika wenten.

## Makontribusi

Bebas ngirimang pikobet utawi pinunas tarik mangda prasida nincapang naskah. Pastikayang pauwahan Sametoné sampun kauji becik sadurung kakirim.

## Lisensi

Proyek puniki polih lisensi ring sor Lisensi MIT - cingak berkas [LICENSE](LICENSE) antuk rinciannyané.

## Cingakin nganggén basa Inggris?

[README-EN](README-en.md)