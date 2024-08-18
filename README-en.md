# UploadGen

`UploadGen` is a Python script designed for easy file uploads to popular file-sharing platforms. This utility simplifies uploading files by providing a straightforward command-line interface.

## Features

- **Upload to PixelDrain**: Requires an API key for authentication.
- **Upload to GoFile**: Automatically selects a server for upload.
- **Upload to Bashupload**: Files are stored for 3 days and can be downloaded only once.
- **Upload to Devuploads**

## Requirements

- Python 3.x
- `requests` library (can be installed via `pip`)

## Installation

1. Clone the repository or download the script file.

   ```bash
   git clone https://github.com/officialputuid/UploadGen.git
   cd UploadGen
   ```

2. Install the required Python library:

   ```bash
   pip install requests
   ```

## Usage

1. **Run the Script**

   ```bash
   python uploadgen.py
   ```

2. **Choose an Upload Service**

   After starting the script, you will be prompted to choose an upload service:

   - **1**: Upload to PixelDrain (API key required)
   - **2**: Upload to GoFile (no API key required)
   - **3**: Upload to Bashupload
   - **4**: Upload to Devuploads (API key required)

3. **Provide Necessary Information**

   - For PixelDrain: Enter your API key when prompted.
   - For GoFile: No API key is needed.
   - For Bashupload: No API key is needed.
   - For Devuploads: Enter your API key when prompted.

4. **Specify the File Path**

   Enter the path to the file you want to upload. The script will validate the file path and proceed with the upload.

## Example

```
UploadGen v1.0
by officialputuid

Choose an UploadGen to:
1. Pixeldrain.com (Need API)
2. GoFile.io
3. Bashupload.com (Can only be used/downloaded once)
4. Devuploads.com (Need API)

Enter the number of your choice: 1
Enter your Pixeldrain API key: your_api_key_here
Enter the path to the file you want to upload: /path/to/your/file.txt
Uploading /path/to/your/file.txt to PixelDrain.com
File uploaded successfully!
Your file URL: https://pixeldrain.com/u/file

Enter the number of your choice: 2
Enter the path to the file you want to upload: /path/to/your/file.txt
Uploading /path/to/your/file.txt to GoFile.io
File uploaded successfully!
Your file URL: https://gofile.io/d/file

Enter the number of your choice: 3
Enter the path to the file you want to upload: /path/to/your/file.txt
Uploading /path/to/your/file.txt to Bashupload.com
File uploaded successfully!
Your file URL: https://bashupload.com/?/file

Enter the number of your choice: 4
Enter the path to the file you want to upload: /path/to/your/file.txt
Uploading /path/to/your/file.txt to Devuploads.com
File uploaded successfully!
Your file URL: https://devuploads.com/file
```

## Error Handling

- **API Key Issues**: Ensure you provide a valid API key for PixelDrain.
- **File Path Issues**: Make sure the file path is correct and the file exists.

## Contributing

Feel free to submit issues or pull requests to improve the script. Please ensure your changes are well-tested before submitting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
