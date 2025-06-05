import typer
import hashlib

app = typer.Typer()

@app.command()
def create(text: str, algo: str = "md5"):

    try:
        hash_func = getattr(hashlib, algo)
        hashed = hash_func(text.encode()).hexdigest()
        typer.echo(f"[🔒] {algo.upper()} → {hashed}")
    except AttributeError:
        typer.echo(f"[❌] Invalid algorithm: {algo}")
