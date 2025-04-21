import hashlib

def crack_hash(hash_value: str, wordlist_path: str, algorithm: str):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if hash_value == hash_password(password, algorithm):
                    print(f"[✅] Erfolgreich: {password}")
                    return
        print("[❌] Kein Passwort gefunden.")
    except FileNotFoundError:
        print(f"[⚠️] Wordlist nicht gefunden: {wordlist_path}")

def hash_password(password: str, algorithm: str):
    """
    Generiert den Hash für ein gegebenes Passwort und den gewünschten Algorithmus.
    """
    try:
        hash_object = hashlib.new(algorithm, password.encode())
        return hash_object.hexdigest()
    except ValueError:
        print(f"[⚠️] Ungültiger Algorithmus: {algorithm}")
        return None
