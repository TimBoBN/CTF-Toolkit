import typer
from core import decoder

app = typer.Typer()

@app.command()
def list():
    """Displays all available decoders."""
    typer.echo("[📦] Available decoders:")
    for name in decoder.decoders.keys():
        typer.echo(f" - {name}")


@app.command()
def run(method: str, input: str):
    """Applies a specific decoder to the input."""
    method = method.strip().capitalize()

    if method not in decoder.decoders:
        typer.echo(f"[❌] Decoder '{method}' not found. Use 'decode list' to show all available decoders.")
        raise typer.Exit()

    result = decoder.decoders[method](input)
    if result and result != input:
        typer.echo(f"[✅ {method}] → {result}")
    else:
        typer.echo(f"[⚠️] No meaningful output from {method}.")
