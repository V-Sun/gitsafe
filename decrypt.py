"""
GitSafe Decryption Module
Handles file decryption with version tracking and metadata updates.
"""
from cryptography.fernet import Fernet
from metadata import mark_decrypted
import sys
import os

KEY_PATH = "keys/secret.key"
ENCRYPTED_DIR = os.path.join("data", "encrypted")
DECRYPTED_DIR = os.path.join("data", "decrypted")


def load_key():
    """Load the encryption key from file."""
    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(
            f"Encryption key not found at {KEY_PATH}. Cannot decrypt without key."
        )
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()


def decrypt_file(filename):
    """
    Decrypt an encrypted file.

    Args:
        filename: Either the full encrypted filename (e.g., "file.v1.enc")
                 or the base filename (e.g., "file.txt") to auto-find next version

    Returns:
        str: Path to the decrypted file
    """
    try:
        key = load_key()
        fernet = Fernet(key)
        os.makedirs(DECRYPTED_DIR, exist_ok=True)

        # Case 1: Full encrypted filename provided (e.g., "file.v1.enc")
        if filename.endswith(".enc"):
            encrypted_path = os.path.join(ENCRYPTED_DIR, filename)
            decrypted_filename = filename.replace(".enc", ".dec")
            decrypted_path = os.path.join(DECRYPTED_DIR, decrypted_filename)

            if not os.path.exists(encrypted_path):
                raise FileNotFoundError(f"Encrypted file not found: {encrypted_path}")

            if os.path.exists(decrypted_path):
                print(f"⚠️  File already decrypted: {decrypted_path}")
                return decrypted_path

        # Case 2: Base filename provided - find the first undecrypted version
        else:
            base_filename = filename
            version = 1
            found = False

            while True:
                encrypted_name = f"{base_filename}.v{version}.enc"
                decrypted_name = f"{base_filename}.v{version}.dec"
                encrypted_path = os.path.join(ENCRYPTED_DIR, encrypted_name)
                decrypted_path = os.path.join(DECRYPTED_DIR, decrypted_name)

                # No more encrypted versions exist
                if not os.path.exists(encrypted_path):
                    break

                # Found an undecrypted version
                if not os.path.exists(decrypted_path):
                    found = True
                    break

                version += 1

            if not found:
                print("⚠️  All encrypted versions have already been decrypted.")
                return None

        # Perform decryption
        with open(encrypted_path, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(decrypted_path, "wb") as dec_file:
            dec_file.write(decrypted)

        print(f"✅ Decrypted: {encrypted_path} → {decrypted_path}")

        # Update metadata
        base = os.path.basename(encrypted_path)
        parts = base.split(".v")

        if len(parts) == 2 and parts[1].endswith(".enc"):
            base_filename = parts[0]
            version_str = parts[1].replace(".enc", "")
            if version_str.isdigit():
                version = int(version_str)
                mark_decrypted(base_filename, version, decrypted_path)
                print(f"📝 Metadata updated for {base_filename}.v{version}")
            else:
                print("⚠️  Could not parse version from filename")
        else:
            print("⚠️  Unexpected filename format - skipping metadata update")

        return decrypted_path

    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <filename>")
        print("Example: python decrypt.py secret.txt")
        print("         python decrypt.py secret.txt.v1.enc")
        sys.exit(1)

    decrypt_file(sys.argv[1])
