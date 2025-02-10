#!/usr/bin/env python3
"""
GitSafe - Secure File Encryption with Version Control

A command-line tool for encrypting, decrypting, and managing versioned encrypted files.
Uses AES-256 encryption via the cryptography library.

Usage:
    python gitsafe.py encrypt <filename>
    python gitsafe.py decrypt <filename>
    python gitsafe.py clear <filename> --keep <num>
    python gitsafe.py list [filename]
    python gitsafe.py init
"""
import argparse
import sys
from encrypt import encrypt_file, generate_key, KEY_PATH
from decrypt import decrypt_file
from clear import clear_versions
from metadata import get_file_versions, list_all_files
import os


def cmd_init():
    """Initialize GitSafe by creating directory structure and encryption key."""
    print("🔧 Initializing GitSafe...")

    # Create directory structure
    directories = [
        "data/files",
        "data/encrypted",
        "data/decrypted",
        "data/metadata",
        "keys",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created: {directory}/")

    # Generate encryption key if it doesn't exist
    if not os.path.exists(KEY_PATH):
        generate_key()
    else:
        print(f"  ⚠️  Encryption key already exists at {KEY_PATH}")

    print("\n✅ GitSafe initialized successfully!")
    print("\n📝 Next steps:")
    print("  1. Place files to encrypt in data/files/")
    print("  2. Run: python gitsafe.py encrypt <filename>")


def cmd_list(filename=None):
    """List all encrypted files or versions of a specific file."""
    if filename:
        versions = get_file_versions(filename)
        if not versions:
            print(f"⚠️  No versions found for '{filename}'")
            return

        print(f"\n📋 Versions of '{filename}':")
        for v in sorted(versions, key=lambda x: x["version"]):
            status = "✅ Decrypted" if v.get("decrypted_path") else "🔒 Encrypted"
            print(f"  v{v['version']}: {status} - {v['timestamp'][:19]}")
    else:
        files = list_all_files()
        if not files:
            print("⚠️  No encrypted files found")
            return

        print("\n📋 Encrypted files:")
        for f in sorted(files):
            versions = get_file_versions(f)
            print(f"  {f} - {len(versions)} version(s)")


def main():
    parser = argparse.ArgumentParser(
        description="GitSafe: Secure file encryption with version control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init                          Initialize GitSafe
  %(prog)s encrypt secret.txt            Encrypt a file
  %(prog)s decrypt secret.txt            Decrypt the latest version
  %(prog)s clear secret.txt --keep 3     Keep only 3 latest versions
  %(prog)s list                          List all encrypted files
  %(prog)s list secret.txt               List versions of a specific file
        """,
    )

    parser.add_argument(
        "command",
        choices=["encrypt", "decrypt", "clear", "list", "init"],
        help="Action to perform",
    )
    parser.add_argument("filename", nargs="?", help="File to operate on")
    parser.add_argument(
        "--keep",
        type=int,
        default=0,
        help="Number of versions to keep (for 'clear' command)",
    )

    args = parser.parse_args()

    try:
        if args.command == "init":
            cmd_init()

        elif args.command == "list":
            cmd_list(args.filename)

        elif args.command in ["encrypt", "decrypt", "clear"]:
            if not args.filename:
                print(f"❌ Error: filename required for '{args.command}' command")
                parser.print_help()
                sys.exit(1)

            if args.command == "encrypt":
                print(f"🔒 Encrypting: {args.filename}")
                encrypt_file(args.filename)

            elif args.command == "decrypt":
                print(f"🔓 Decrypting: {args.filename}")
                decrypt_file(args.filename)

            elif args.command == "clear":
                print(f"🗑️  Clearing versions of '{args.filename}', keeping {args.keep}...")
                clear_versions(args.filename, keep=args.keep)

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

