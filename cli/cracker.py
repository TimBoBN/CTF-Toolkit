### cli/cracker.py
import typer
import sys
import os

# Add root dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.cracker import crack_hash

app = typer.Typer()

@app.command()
def hash(hash: str, wordlist: str):
    """
    Crackt einfachen MD5 Hash gegen eine Wordlist.
    Du musst nur den Namen der Wordlist angeben, z. B. 'rockyou.txt'
    """
    wordlist_path = os.path.join("wordlist", wordlist)
    typer.echo(f"[🔍] Analysiere Hash: {hash} mit Wordlist: {wordlist_path}")
    crack_hash(hash, wordlist_path)
