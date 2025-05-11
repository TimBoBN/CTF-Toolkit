import typer
import re

app = typer.Typer()

@app.command()
def search(pattern: str, text: str):
    """
    Searches for a pattern in the text using a regex.
    """
    matches = re.findall(pattern, text)
    if matches:
        typer.echo(f"[🔍] Found: {matches}")
    else:
        typer.echo("[❌] No matches found.")