import typer
import sys
import os

# Add root dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.cracker import crack_hash

app = typer.Typer()

@app.command()
def hash(hash: str, wordlist: str, algorithm: str = typer.Option("md5", "-a", "--algorithm", help="Der zu verwendende Hash-Algorithmus")):
    """
    Crackt einen Hash gegen eine Wordlist mit einem angegebenen Algorithmus.
    Der Benutzer muss den Hash-Algorithmus und den Namen der Wordlist angeben, z. B. 'rockyou.txt'.
    Standardmäßig wird MD5 verwendet.
    """
    # Debug-Ausgabe zur Überprüfung
    typer.echo(f"[🔍] Hash: {hash}")
    typer.echo(f"[🔍] Wordlist: {wordlist}")
    typer.echo(f"[🔍] Algorithmus: {algorithm}")
    
    wordlist_path = os.path.join("wordlist", wordlist)
    typer.echo(f"[🔍] Wordlist-Pfad: {wordlist_path}")
    
    # Funktionsaufruf
    crack_hash(hash, wordlist_path, algorithm)
