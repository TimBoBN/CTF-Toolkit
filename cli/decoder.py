import typer

app = typer.Typer()

@app.command()
def base64(text: str):
    """
    Decodiert Base64-Text.
    """
    import base64
    try:
        decoded = base64.b64decode(text).decode("utf-8")
        typer.echo(f"[🔓] Base64 → {decoded}")
    except Exception as e:
        typer.echo(f"[❌] Fehler beim Decodieren: {e}")
