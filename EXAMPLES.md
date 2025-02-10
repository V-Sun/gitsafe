# GitSafe Usage Examples

This document provides detailed examples and common workflows for using GitSafe.

## Table of Contents
- [Basic Workflow](#basic-workflow)
- [Managing Multiple Files](#managing-multiple-files)
- [Version Control Scenarios](#version-control-scenarios)
- [Advanced Usage](#advanced-usage)
- [Common Patterns](#common-patterns)

## Basic Workflow

### First-Time Setup

```bash
# 1. Initialize GitSafe
python gitsafe.py init

# Output:
# 🔧 Initializing GitSafe...
#   ✅ Created: data/files/
#   ✅ Created: data/encrypted/
#   ✅ Created: data/decrypted/
#   ✅ Created: data/metadata/
#   ✅ Created: keys/
# ✅ Generated new encryption key at keys/secret.key
#
# ✅ GitSafe initialized successfully!
```

### Encrypting Your First File

```bash
# 1. Create a file with sensitive content
echo "API_KEY=sk-1234567890abcdef" > data/files/secrets.env

# 2. Encrypt it
python gitsafe.py encrypt secrets.env

# Output:
# 🔒 Encrypting: secrets.env
# ✅ Encrypted 'secrets.env' → data/encrypted/secrets.env.v1.enc
```

### Decrypting a File

```bash
# Decrypt the file
python gitsafe.py decrypt secrets.env

# Output:
# 🔓 Decrypting: secrets.env
# ✅ Decrypted: data/encrypted/secrets.env.v1.enc → data/decrypted/secrets.env.v1.dec
# 📝 Metadata updated for secrets.env.v1
```

## Managing Multiple Files

### Encrypting Multiple Files

```bash
# Create multiple sensitive files
echo "DATABASE_URL=postgres://..." > data/files/db_config.txt
echo "JWT_SECRET=supersecret123" > data/files/auth_config.txt
echo "AWS_KEY=AKIA..." > data/files/aws_credentials.txt

# Encrypt each file
python gitsafe.py encrypt db_config.txt
python gitsafe.py encrypt auth_config.txt
python gitsafe.py encrypt aws_credentials.txt

# List all encrypted files
python gitsafe.py list

# Output:
# 📋 Encrypted files:
#   auth_config.txt - 1 version(s)
#   aws_credentials.txt - 1 version(s)
#   db_config.txt - 1 version(s)
#   secrets.env - 1 version(s)
```

## Version Control Scenarios

### Creating Multiple Versions

```bash
# Create initial version
echo "version 1 data" > data/files/config.json
python gitsafe.py encrypt config.json
# Creates: config.json.v1.enc

# Update the file and encrypt again
echo "version 2 data" > data/files/config.json
python gitsafe.py encrypt config.json
# Creates: config.json.v2.enc

# Update again
echo "version 3 data" > data/files/config.json
python gitsafe.py encrypt config.json
# Creates: config.json.v3.enc

# View all versions
python gitsafe.py list config.json

# Output:
# 📋 Versions of 'config.json':
#   v1: 🔒 Encrypted - 2025-02-10 10:00:00
#   v2: 🔒 Encrypted - 2025-02-10 10:05:00
#   v3: 🔒 Encrypted - 2025-02-10 10:10:00
```

### Decrypting Specific Versions

```bash
# Decrypt the latest version (v3)
python gitsafe.py decrypt config.json

# Decrypt a specific version
python gitsafe.py decrypt config.json.v1.enc
python gitsafe.py decrypt config.json.v2.enc
```

### Cleaning Up Old Versions

```bash
# Keep only the 2 most recent versions
python gitsafe.py clear config.json --keep 2

# Output:
# Found 3 version(s). Keeping 2, removing 1.
#   🗑️  Deleted: data/encrypted/config.json.v1.enc
# ✅ Cleanup complete: Deleted 1 encrypted and 0 decrypted version(s) of 'config.json'. Kept 2.

# Verify
python gitsafe.py list config.json

# Output:
# 📋 Versions of 'config.json':
#   v2: 🔒 Encrypted - 2025-02-10 10:05:00
#   v3: 🔒 Encrypted - 2025-02-10 10:10:00
```

## Advanced Usage

### Backup and Restore Workflow

```bash
# 1. Encrypt important files before backup
python gitsafe.py encrypt important_data.json
python gitsafe.py encrypt private_keys.pem

# 2. Back up encrypted files to cloud storage
# (encrypted files can be safely stored anywhere)
cp data/encrypted/* ~/Dropbox/encrypted_backup/
cp keys/secret.key ~/secure_location/secret.key.backup

# 3. To restore on another machine:
# - Copy encrypted files to data/encrypted/
# - Copy secret.key to keys/
# - Run decrypt
python gitsafe.py decrypt important_data.json
```

### Configuration File Versioning

```bash
# Development configuration
echo '{"env": "dev", "debug": true}' > data/files/app_config.json
python gitsafe.py encrypt app_config.json

# Staging configuration
echo '{"env": "staging", "debug": false}' > data/files/app_config.json
python gitsafe.py encrypt app_config.json

# Production configuration
echo '{"env": "prod", "debug": false}' > data/files/app_config.json
python gitsafe.py encrypt app_config.json

# Now you have 3 versions representing different environments
python gitsafe.py list app_config.json

# Decrypt specific version for deployment
python gitsafe.py decrypt app_config.json.v3.enc  # Production config
```

### Rotating API Keys

```bash
# Old API key
echo "API_KEY=old_key_123" > data/files/api_keys.txt
python gitsafe.py encrypt api_keys.txt

# New API key (after rotation)
echo "API_KEY=new_key_456" > data/files/api_keys.txt
python gitsafe.py encrypt api_keys.txt

# Keep both versions for a transition period
python gitsafe.py list api_keys.txt

# After transition, keep only the new key
python gitsafe.py clear api_keys.txt --keep 1
```

## Common Patterns

### Pattern 1: Daily Encrypted Backups

```bash
#!/bin/bash
# Script: daily_backup.sh

# Encrypt today's important files
python gitsafe.py encrypt daily_report.txt
python gitsafe.py encrypt transaction_log.csv

# Keep last 7 days
python gitsafe.py clear daily_report.txt --keep 7
python gitsafe.py clear transaction_log.csv --keep 7

# List what's stored
python gitsafe.py list
```

### Pattern 2: Environment-Specific Secrets

```bash
# .env.development
echo "DB_HOST=localhost" > data/files/.env
python gitsafe.py encrypt .env
mv data/encrypted/.env.v1.enc data/encrypted/.env.development.v1.enc

# .env.production
echo "DB_HOST=prod.example.com" > data/files/.env
python gitsafe.py encrypt .env
mv data/encrypted/.env.v2.enc data/encrypted/.env.production.v2.enc
```

### Pattern 3: Secure Code Review

```bash
# Encrypt code before sharing for review
python gitsafe.py encrypt sensitive_algorithm.py

# Share encrypted file and key separately
# Reviewer decrypts:
python gitsafe.py decrypt sensitive_algorithm.py

# After review, clean up
python gitsafe.py clear sensitive_algorithm.py --keep 0
```

## Error Handling Examples

### Missing Key

```bash
# If key is missing
python gitsafe.py encrypt test.txt

# Output:
# 🔒 Encrypting: test.txt
# 🔑 No encryption key found. Generating a new one...
# ✅ Generated new encryption key at keys/secret.key
# ✅ Encrypted 'test.txt' → data/encrypted/test.txt.v1.enc
```

### File Not Found

```bash
python gitsafe.py encrypt nonexistent.txt

# Output:
# 🔒 Encrypting: nonexistent.txt
# ❌ Encryption failed: Input file not found: data/files/nonexistent.txt
```

### Already Decrypted

```bash
# Decrypt the same file twice
python gitsafe.py decrypt test.txt
python gitsafe.py decrypt test.txt

# Output (second time):
# 🔓 Decrypting: test.txt
# ⚠️  All encrypted versions have already been decrypted.
```

## Tips and Best Practices

1. **Always backup your encryption key** (`keys/secret.key`)
2. **Use version control for encrypted files** (they're safe to commit)
3. **Clean up old versions regularly** to save space
4. **Use descriptive filenames** for better organization
5. **Keep sensitive files out of `data/files/`** after encryption
6. **Test decryption** before deleting original files

## Scripting with GitSafe

### Python Script Example

```python
#!/usr/bin/env python3
import subprocess
import sys

def encrypt_all_configs():
    """Encrypt all configuration files"""
    configs = ['app.json', 'database.json', 'secrets.env']

    for config in configs:
        result = subprocess.run(
            ['python', 'gitsafe.py', 'encrypt', config],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Encrypted {config}")
        else:
            print(f"❌ Failed to encrypt {config}")
            print(result.stderr)

if __name__ == "__main__":
    encrypt_all_configs()
```

### Bash Script Example

```bash
#!/bin/bash
# Encrypt all .env files

for file in data/files/*.env; do
    filename=$(basename "$file")
    echo "Encrypting $filename..."
    python gitsafe.py encrypt "$filename"
done

echo "Listing all encrypted files:"
python gitsafe.py list
```

---

For more information, see the [README.md](README.md) file.
