# UploadGen

**UploadGen** is a versatile Python script designed to simplify file uploads to popular file-sharing platforms through an intuitive command-line interface.

## Features

- **Upload to Pixeldrain**: Upload files with API key authentication.
- **Upload to GoFile**: Automatically selects an appropriate server for uploading.
- **Upload to Bashupload**: Files are stored for 3 days and can be downloaded only once.
- **Upload to Devuploads**: Requires API key authentication for file uploads.

## Requirements

- Python 3.x
- `requests` library (installable via `pip`)

## Installation

To get started with UploadGen, follow these steps:

   ```bash
   git clone https://github.com/officialputuid/UploadGen.git
   cd UploadGen
   python3 uploadgen.py or python uploadgen.py -s [1/2/3/4/5] -f [file]
   ```

Alternatively, you can download the script directly:

   ```bash
   wget https://raw.githubusercontent.com/officialputuid/UploadGen/main/uploadgen.py
   python3 uploadgen.py / python uploadgen.py -s [1/2/3/4/5] -f [file]
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
   python uploadgen.py -s [1/2/3/4/5] -f [file]
   ```
   ex: `python uploadgen.py -s 2 -f /path/file.txt`

- `-h`: UploadGen Guide
- `-s [1/2/3/4]`: Select service:
  - `1` for Pixeldrain.com
  - `2` for GoFile.io
  - `3` for Bashupload.com
  - `4` for Devuploads.com
  - `5` for File.io
- `-f [file]`: Specifies the path to the file you want to upload.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
