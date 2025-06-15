from cryptography.fernet import Fernet
import sys
import os

KEY_PATH = "keys/secret.key"

def load_key():
    return open(KEY_PATH, "rb").read()

def decrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)
    file_path = os.path.join("data", "encrypted", filename)
    with open(file_path, "rb") as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)

    file_path = os.path.join("data", "decrypted", filename)
    original_name = file_path.replace(".enc", "")
    with open(original_name + ".dec", "wb") as dec_file:
        dec_file.write(decrypted)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <filename>")
        sys.exit(1)

    decrypt_file(sys.argv[1])
