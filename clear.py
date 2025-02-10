"""
GitSafe Clear Module
Handles cleanup of old file versions while keeping the most recent ones.
"""
import os
from metadata import read_metadata, write_metadata

ENCRYPTED_DIR = os.path.join("data", "encrypted")
DECRYPTED_DIR = os.path.join("data", "decrypted")


def clear_versions(filename, keep=0):
    """
    Clear old versions of a file, keeping only the most recent ones.

    Args:
        filename: Name of the file to clear versions for
        keep: Number of most recent versions to keep (default: 0 - delete all)

    Returns:
        dict: Summary of deleted files
    """
    data = read_metadata()

    # Filter entries for the specified file
    relevant = [entry for entry in data if entry["filename"] == filename]

    if not relevant:
        print(f"⚠️  No encrypted versions found for '{filename}'")
        return {"deleted_encrypted": 0, "deleted_decrypted": 0}

    # Sort by version (newest first)
    relevant.sort(key=lambda x: x["version"], reverse=True)

    to_keep = relevant[:keep]
    to_remove = relevant[keep:]

    print(f"Found {len(relevant)} version(s). Keeping {len(to_keep)}, removing {len(to_remove)}.")

    deleted_enc = 0
    deleted_dec = 0

    # Delete files
    for entry in to_remove:
        enc_path = entry.get("encrypted_path")
        dec_path = entry.get("decrypted_path")

        if enc_path and os.path.exists(enc_path):
            os.remove(enc_path)
            deleted_enc += 1
            print(f"  🗑️  Deleted: {enc_path}")

        if dec_path and os.path.exists(dec_path):
            os.remove(dec_path)
            deleted_dec += 1
            print(f"  🗑️  Deleted: {dec_path}")

    # Update metadata
    updated = [entry for entry in data if entry not in to_remove]
    write_metadata(updated)

    print(
        f"✅ Cleanup complete: Deleted {deleted_enc} encrypted and {deleted_dec} "
        f"decrypted version(s) of '{filename}'. Kept {len(to_keep)}."
    )

    return {"deleted_encrypted": deleted_enc, "deleted_decrypted": deleted_dec}

        

              