import typer
import requests
from pathlib import Path
from core import decoder

app = typer.Typer()

@app.command("auto")
def auto_scan(file: Path):
    if not file.exists():
        typer.echo(f"[❌] File not found: {file}")
        raise typer.Exit()

    typer.echo(f"[🔍] Auto-scan started: {file.name}\n")
    content = file.read_text(encoding="utf-8", errors="ignore")

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue

        for name, func in decoder.decoders.items():
            result = func(line)
            if result and result != line:
                typer.echo(f"[✅ {name}] {line} → {result}")