### main.py
import typer
import sys
import os

# Add root dir to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from cli import cracker, decoder, regex, hasher, scanner, url_scanner, recon, vulnscaner

app = typer.Typer()

# Sub-Kommandos registrieren
app.add_typer(cracker.app, name="crack")
app.add_typer(decoder.app, name="decode")
app.add_typer(regex.app, name="regex")
app.add_typer(hasher.app, name="hash")
app.add_typer(scanner.app, name="scan")
app.add_typer(url_scanner.app, name="url")
app.add_typer(recon.app, name="recon")
app.add_typer(vulnscaner.app, name="vulnscan")

if __name__ == "__main__":
    app()