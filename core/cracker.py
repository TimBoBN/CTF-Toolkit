import hashlib
import os

def crack_hash(hash_value: str, wordlist_path: str, algorithm: str):
    print(f"[🔍] Starte das Knacken des Hashes: {hash_value} mit Algorithmus: {algorithm}")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if hash_value == hash_password(password, algorithm):
                    print(f"[✅] Erfolgreich: {password} mit Algorithmus {algorithm}")
                    return
        print(f"[❌] Kein Passwort gefunden mit Algorithmus {algorithm}.")
    except FileNotFoundError:
        print(f"[⚠️] Wordlist nicht gefunden: {wordlist_path}")

def hash_password(password: str, algorithm: str):
    """
    Generiert den Hash für ein gegebenes Passwort und den gewünschten Algorithmus.
    """
    try:
        # Überprüfen, ob der Algorithmus unterstützt wird
        if algorithm not in hashlib.algorithms_guaranteed:
            print(f"[⚠️] Ungültiger Algorithmus: {algorithm}")
            return None
        
        hash_object = hashlib.new(algorithm, password.encode())
        hashed_password = hash_object.hexdigest()
        
        # Debug-Ausgabe für den generierten Hash
        return hashed_password
    except ValueError as e:
        print(f"[⚠️] Fehler bei der Verwendung des Algorithmus: {algorithm}. {str(e)}")
        return None
