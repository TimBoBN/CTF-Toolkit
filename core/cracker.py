import hashlib
import os

def crack_hash(hash_value: str, wordlist_path: str, algorithm: str):
    print(f"[🔍] Starting to crack the hash: {hash_value} using algorithm: {algorithm}")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if hash_value == hash_password(password, algorithm):
                    print(f"[✅] Success: {password} with algorithm {algorithm}")
                    return
        print(f"[❌] No password found with algorithm {algorithm}.")
    except FileNotFoundError:
        print(f"[⚠️] Wordlist not found: {wordlist_path}")

def hash_password(password: str, algorithm: str):
    """
    Generates the hash for a given password using the specified algorithm.
    """
    try:
        # Check if algorithm is supported
        if algorithm not in hashlib.algorithms_guaranteed:
            print(f"[⚠️] Invalid algorithm: {algorithm}")
            return None
        
        hash_object = hashlib.new(algorithm, password.encode())
        hashed_password = hash_object.hexdigest()
        
        return hashed_password
    except ValueError as e:
        print(f"[⚠️] Error using algorithm: {algorithm}. {str(e)}")
        return None
