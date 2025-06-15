# GitSafe 

A secure, version-controlled encryption tool for storing sensitive code and files.

## Features
- AES-256 encryption using `cryptography`'s Fernet
- Command-line `encrypt.py` and `decrypt.py`
- Auto key generation and management
- Modular file structure

## Usage
```bash
# Encrypt a file
python encrypt.py data/secret.txt

# Decrypt a file
python decrypt.py data/secret.txt.enc
