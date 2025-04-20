import typer
from core.cracker import crack_hash

app = typer.Typer()

@app.command()
def hash(hash: str, wordlist: str):
    """Crackt einfachen MD5 Hash gegen eine Wordlist."""
    typer.echo(f"[🔍] Analysiere Hash: {hash}")
    crack_hash(hash, wordlist)
