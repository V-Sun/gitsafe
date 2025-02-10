# 🔒 GitSafe

**Secure file encryption with automatic versioning and metadata tracking**

GitSafe is a Python-based command-line tool that provides military-grade AES-256 encryption for your sensitive files. With built-in version control, you can encrypt files multiple times, track changes, and manage different versions seamlessly.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔐 **AES-256 Encryption**: Industry-standard encryption using the `cryptography` library
- 📦 **Automatic Versioning**: Keep multiple encrypted versions of the same file
- 📋 **Metadata Tracking**: JSON-based metadata for all encrypted/decrypted files
- 🗑️ **Version Management**: Clean up old versions while keeping recent ones
- 🎯 **Simple CLI**: Easy-to-use command-line interface
- 🔑 **Key Management**: Automatic encryption key generation and storage
- 📊 **File Listing**: View all encrypted files and their versions

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/GitSafe.git
   cd GitSafe
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize GitSafe**
   ```bash
   python gitsafe.py init
   ```

### Basic Usage

```bash
# Encrypt a file
python gitsafe.py encrypt secrets.txt

# Decrypt a file
python gitsafe.py decrypt secrets.txt

# List all encrypted files
python gitsafe.py list

# List versions of a specific file
python gitsafe.py list secrets.txt

# Clean up old versions (keep only 3 most recent)
python gitsafe.py clear secrets.txt --keep 3
```

## 📖 Detailed Usage

### Encrypting Files

Place your file in `data/files/` and run:
```bash
python gitsafe.py encrypt myfile.txt
```

This will:
- Encrypt the file using AES-256
- Save it to `data/encrypted/` with version number (e.g., `myfile.txt.v1.enc`)
- Update metadata in `data/metadata/metadata.json`

### Decrypting Files

```bash
# Decrypt by base filename (finds the first undecrypted version)
python gitsafe.py decrypt myfile.txt

# Decrypt a specific version
python gitsafe.py decrypt myfile.txt.v1.enc
```

Decrypted files are saved to `data/decrypted/` with a `.dec` extension.

### Managing Versions

GitSafe automatically creates new versions when you encrypt the same file multiple times:

```bash
python gitsafe.py encrypt config.json  # Creates config.json.v1.enc
python gitsafe.py encrypt config.json  # Creates config.json.v2.enc
python gitsafe.py encrypt config.json  # Creates config.json.v3.enc
```

Clean up old versions:
```bash
# Keep only the 2 most recent versions
python gitsafe.py clear config.json --keep 2

# Delete all versions
python gitsafe.py clear config.json --keep 0
```

### Listing Files

```bash
# List all encrypted files
python gitsafe.py list

# Output:
# 📋 Encrypted files:
#   config.json - 3 version(s)
#   secrets.txt - 1 version(s)

# List versions of a specific file
python gitsafe.py list config.json

# Output:
# 📋 Versions of 'config.json':
#   v1: ✅ Decrypted - 2025-02-10 14:30:00
#   v2: ✅ Decrypted - 2025-02-10 15:45:00
#   v3: 🔒 Encrypted - 2025-02-10 16:20:00
```

## 🗂️ Project Structure

```
GitSafe/
├── gitsafe.py          # Main CLI interface
├── encrypt.py          # Encryption module
├── decrypt.py          # Decryption module
├── metadata.py         # Metadata management
├── clear.py            # Version cleanup
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # MIT License
│
├── data/
│   ├── files/         # Place files to encrypt here
│   ├── encrypted/     # Encrypted files stored here
│   ├── decrypted/     # Decrypted files stored here
│   └── metadata/      # Metadata JSON files
│
└── keys/
    └── secret.key     # Encryption key (auto-generated)
```

## 🔑 Security Considerations

- **Keep your key safe**: The `keys/secret.key` file is critical for decryption. Back it up securely.
- **Never commit keys**: The `.gitignore` file excludes `keys/` and `data/` by default.
- **AES-256 encryption**: Uses Fernet (AES-128 CBC + HMAC) from the `cryptography` library.
- **Version control**: GitSafe is designed to work alongside Git but keeps sensitive data encrypted.

## 🛠️ Development

### Running Tests

```bash
# Place a test file
echo "Hello, World!" > data/files/test.txt

# Test encryption
python gitsafe.py encrypt test.txt

# Test decryption
python gitsafe.py decrypt test.txt

# Verify the decrypted content
cat data/decrypted/test.txt.v1.dec
```

### Module Documentation

Each module includes comprehensive docstrings:

- **encrypt.py**: Handles file encryption with automatic versioning
- **decrypt.py**: Handles file decryption with version detection
- **metadata.py**: Manages JSON metadata for tracking file versions
- **clear.py**: Cleanup utility for managing old versions
- **gitsafe.py**: Main CLI with argparse interface

## 📊 Use Cases

- **API Keys & Credentials**: Encrypt sensitive configuration files
- **Personal Documents**: Secure tax returns, legal documents, etc.
- **Code Secrets**: Protect `.env` files and private keys
- **Version History**: Keep encrypted snapshots of important files
- **Secure Backups**: Encrypt files before pushing to cloud storage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [cryptography](https://cryptography.io/) - A Python library for encryption
- Inspired by the need for simple, version-controlled file encryption

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for secure file management**
