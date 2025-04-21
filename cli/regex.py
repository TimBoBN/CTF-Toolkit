import typer
import re

app = typer.Typer()

@app.command()
def search(pattern: str, text: str):
    """
    Sucht mit einem Regex nach einem Muster im Text.
    """
    matches = re.findall(pattern, text)
    if matches:
        typer.echo(f"[🔍] Gefunden: {matches}")
    else:
        typer.echo("[❌] Keine Übereinstimmungen gefunden.")
