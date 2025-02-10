"""
GitSafe Metadata Module
Manages metadata tracking for encrypted/decrypted file versions.
"""
import json
import os
from datetime import datetime

METADATA_FILE = os.path.join("data", "metadata", "metadata.json")


def read_metadata():
    """
    Read metadata from JSON file.

    Returns:
        list: List of metadata entries
    """
    if not os.path.exists(METADATA_FILE):
        return []

    if os.path.getsize(METADATA_FILE) == 0:
        return []

    try:
        with open(METADATA_FILE, "r") as reader:
            return json.load(reader)
    except json.JSONDecodeError:
        print(f"⚠️  Warning: Corrupted metadata file. Creating new one.")
        return []


def write_metadata(data):
    """
    Write metadata to JSON file.

    Args:
        data: List of metadata entries
    """
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, "w") as writer:
        json.dump(data, writer, indent=4)


def add_entry(filename, version, encrypted_path):
    """
    Add a new encryption entry to metadata.

    Args:
        filename: Original filename
        version: Version number
        encrypted_path: Path to encrypted file
    """
    data = read_metadata()

    entry = {
        "filename": filename,
        "version": version,
        "encrypted_path": encrypted_path,
        "decrypted_path": None,
        "timestamp": datetime.now().isoformat(),
    }

    data.append(entry)
    write_metadata(data)


def mark_decrypted(filename, version, decrypted_path):
    """
    Mark a file version as decrypted in metadata.

    Args:
        filename: Original filename
        version: Version number
        decrypted_path: Path to decrypted file
    """
    data = read_metadata()
    for entry in data:
        if entry["filename"] == filename and entry["version"] == version:
            entry["decrypted_path"] = decrypted_path
            break
    write_metadata(data)


def get_file_versions(filename):
    """
    Get all versions of a specific file.

    Args:
        filename: Original filename

    Returns:
        list: List of version entries for the file
    """
    data = read_metadata()
    return [entry for entry in data if entry["filename"] == filename]


def list_all_files():
    """
    Get a list of all unique filenames in metadata.

    Returns:
        list: Unique filenames
    """
    data = read_metadata()
    return list(set(entry["filename"] for entry in data))


