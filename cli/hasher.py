import typer
import hashlib

app = typer.Typer()

@app.command()
def create(text: str, algo: str = "md5"):
    """
    Erstellt einen Hash aus einem Text. Standard ist MD5.
    Verfügbare Optionen: md5, sha1, sha256, sha512
    """
    try:
        hash_func = getattr(hashlib, algo)
        hashed = hash_func(text.encode()).hexdigest()
        typer.echo(f"[🔒] {algo.upper()} → {hashed}")
    except AttributeError:
        typer.echo(f"[❌] Ungültiger Algorithmus: {algo}")
