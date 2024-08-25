# UploadGen

**UploadGen** is a versatile Python script designed to simplify file uploads to popular file-sharing platforms through an intuitive command-line interface.

## Features

- **Upload to Pixeldrain.com**
- **Upload to GoFile.io**
- **Upload to Bashupload.com**
- **Upload to Devuploads.com**
- **Upload to File.io**
- **Upload to Uguu.se**
- **Upload to 0x0.st**

## Requirements

- Python 3.x
- `requests` library (installable via `pip`)

## Installation

To get started with UploadGen, follow these steps:

   ```bash
   git clone https://github.com/officialputuid/UploadGen.git
   cd UploadGen
   ```

Alternatively, you can download the script directly:

   ```bash
   wget https://raw.githubusercontent.com/officialputuid/UploadGen/main/uploadgen.py
   ```

## Usage

1. **Interactive Mode**

   To start the script and use the interactive menu:

   ```bash
   python uploadgen.py
   ```

2. **Command-Line Arguments**

   To upload a file directly via command-line arguments:

   ```bash
   python uploadgen.py -s [1/2/3/4/5/6/7] -f [file]
   ```
   ex: `python uploadgen.py -s 2 -f /path/file.txt`

- `-h`: UploadGen Guide
- `-s [1/2/3/4/5/6/7]`: Select service:
  - `1` for Pixeldrain.com
  - `2` for GoFile.io
  - `3` for Bashupload.com
  - `4` for Devuploads.com
  - `5` for File.io
  - `7` for 0x0.st
- `-f [file]`: Specifies the path to the file you want to upload.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
