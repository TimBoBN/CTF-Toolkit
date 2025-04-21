### core/cracker.py
def crack_hash(hash_value: str, wordlist_path: str):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if hash_value == fake_md5(password):
                    print(f"[✅] Erfolgreich: {password}")
                    return
        print("[❌] Kein Passwort gefunden.")
    except FileNotFoundError:
        print(f"[⚠️] Wordlist nicht gefunden: {wordlist_path}")


def fake_md5(password: str):
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()
