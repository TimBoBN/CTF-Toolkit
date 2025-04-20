import subprocess
import tempfile
import os

def crack_with_hashcat(hash_value, wordlist_path, hash_mode):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as hashfile:
        hashfile.write(hash_value)
        hashfile_path = hashfile.name

    try:
        subprocess.run([
            "hashcat", "-a", "0", "-m", str(hash_mode),
            hashfile_path, wordlist_path,
            "--quiet", "--force"
        ], check=True)

        subprocess.run([
            "hashcat", "-m", str(hash_mode),
            hashfile_path, "--show"
        ], check=True)

    finally:
        os.remove(hashfile_path)
