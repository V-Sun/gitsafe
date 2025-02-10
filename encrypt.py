"""
GitSafe Encryption Module
Handles file encryption with versioning and metadata tracking.
"""
from cryptography.fernet import Fernet
from metadata import add_entry
import sys
import os

KEY_PATH = "keys/secret.key"
FILES_DIR = os.path.join("data", "files")
ENCRYPTED_DIR = os.path.join("data", "encrypted")


def generate_key():
    """Generate a new encryption key and save it to the key file."""
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    print(f"✅ Generated new encryption key at {KEY_PATH}")


def load_key():
    """Load the encryption key from file."""
    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(
            f"Encryption key not found at {KEY_PATH}. Generate one first."
        )
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()


def encrypt_file(filename):
    """
    Encrypt a file with automatic versioning.

    Args:
        filename: Name of the file to encrypt (relative to data/files/)

    Returns:
        str: Path to the encrypted file
    """
    try:
        key = load_key()
        fernet = Fernet(key)

        input_path = os.path.join(FILES_DIR, filename)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Read original file
        with open(input_path, "rb") as file:
            original = file.read()

        # Encrypt content
        encrypted = fernet.encrypt(original)

        # Find next available version number
        os.makedirs(ENCRYPTED_DIR, exist_ok=True)
        version = 1
        output_path = os.path.join(ENCRYPTED_DIR, f"{filename}.v{version}.enc")
        while os.path.exists(output_path):
            version += 1
            output_path = os.path.join(ENCRYPTED_DIR, f"{filename}.v{version}.enc")

        # Write encrypted file
        with open(output_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        # Update metadata
        add_entry(filename=filename, version=version, encrypted_path=output_path)

        print(f"✅ Encrypted '{filename}' → {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Encryption failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if not os.path.exists(KEY_PATH):
        print("🔑 No encryption key found. Generating a new one...")
        generate_key()

    if len(sys.argv) < 2:
        print("Usage: python encrypt.py <filename>")
        print("Example: python encrypt.py secret.txt")
        sys.exit(1)

    encrypt_file(sys.argv[1])