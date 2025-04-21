import typer
from core import decoder

app = typer.Typer()

@app.command()
def list():
    """Zeigt alle verfügbaren Decoder an."""
    typer.echo("[📦] Verfügbare Decoder:")
    for name in decoder.decoders.keys():
        typer.echo(f" - {name}")


@app.command()
def run(method: str, input: str):
    """Wendet einen bestimmten Decoder auf den Input an."""
    method = method.strip().capitalize()

    if method not in decoder.decoders:
        typer.echo(f"[❌] Decoder '{method}' nicht gefunden. Nutze 'decode list', um alle anzuzeigen.")
        raise typer.Exit()

    result = decoder.decoders[method](input)
    if result and result != input:
        typer.echo(f"[✅ {method}] → {result}")
    else:
        typer.echo(f"[⚠️] Keine sinnvolle Ausgabe durch {method}.")
