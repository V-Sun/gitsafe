from cryptography.fernet import Fernet
import sys
import os

KEY_PATH = "keys/secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

def load_key():
    return open(KEY_PATH, "rb").read()

def encrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    input_path = os.path.join("data", "files", filename)

    with open(input_path, "rb") as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)
    
    num = 1
    base_output = os.path.join("data", "encrypted", f"{filename}.v{num}.enc")
    while os.path.exists(base_output):
        num += 1
        base_output = os.path.join("data", "encrypted", f"{filename}.v{num}.enc")

    with open(base_output, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

if __name__ == "__main__":
    if not os.path.exists(KEY_PATH):
        generate_key()
    
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py <filename>")
        sys.exit(1)

    encrypt_file(sys.argv[1])