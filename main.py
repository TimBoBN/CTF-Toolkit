import typer
from cli import cracker, decoder, regex, hasher

app = typer.Typer()

# Sub-Kommandos als Gruppen
app.add_typer(cracker.app, name="crack")
app.add_typer(decoder.app, name="decode")
app.add_typer(regex.app, name="regex")
app.add_typer(hasher.app, name="hash")

if __name__ == "__main__":
    app()
