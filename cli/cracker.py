import typer
import os
from core.cracker import crack_hash
import hashlib
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

app = typer.Typer()

# Hole die Umgebungsvariablen aus der .env-Datei oder setze Standardwerte
default_algorithm = os.getenv("DEFAULT_ALGORITHM", "auto")
default_wordlist = os.getenv("DEFAULT_WORDLIST", "rockyou.txt")
auto_wordlist_dir = os.getenv("AUTO_WORDLIST_DIR", "auto_wordlists")  # Der Ordner für die Auto-Wordlisten

@app.command()
def hash(
    hash: str,
    wordlist: str = typer.Option(None, "-w", "--wordlist", help="Die zu verwendende Wordlist. Wenn nicht angegeben, wird die Standard- oder Auto-Wordlist verwendet."),
    algorithm: str = typer.Option(default_algorithm, "-a", "--algorithm", help="Der zu verwendende Hash-Algorithmus. Wenn 'auto', werden alle Algorithmen ausprobiert.")
):
    """
    Crackt einen Hash gegen eine Wordlist mit einem angegebenen oder allen unterstützten Hash-Algorithmen.
    """
    if algorithm == "auto":
        algorithms_to_test = hashlib.algorithms_guaranteed
        typer.echo("[🔍] Alle unterstützten Algorithmen werden ausprobiert: " + ", ".join(algorithms_to_test))
        
        # Lade alle Wordlisten im angegebenen Ordner für den Auto-Modus
        wordlist_files = [f for f in os.listdir(auto_wordlist_dir) if os.path.isfile(os.path.join(auto_wordlist_dir, f))]
        
        if not wordlist_files:
            typer.echo(f"[⚠️] Keine Wordlisten im Auto-Ordner gefunden: {auto_wordlist_dir}")
            return
        
        typer.echo(f"[🔍] Verwende Auto-Wordlisten aus dem Ordner: {auto_wordlist_dir}")
    elif algorithm:
        algorithms_to_test = [algorithm]
        typer.echo(f"[🔍] Nur der Algorithmus {algorithm} wird ausprobiert.")
        wordlist_to_use = wordlist if wordlist else default_wordlist  # Verwende die Standard-Wordlist oder eine benutzerdefinierte
        typer.echo(f"[🔍] Verwende Wordlist: {wordlist_to_use}")
    else:
        algorithms_to_test = hashlib.algorithms_guaranteed
        typer.echo("[🔍] Alle unterstützten Algorithmen werden ausprobiert.")
        wordlist_to_use = wordlist if wordlist else default_wordlist  # Verwende die Standard-Wordlist oder eine benutzerdefinierte

    # Wenn der Modus 'auto' ist, verwenden wir die Wordlisten aus dem Ordner
    if algorithm == "auto":
        for wordlist_name in wordlist_files:
            wordlist_path = os.path.join(auto_wordlist_dir, wordlist_name)
            typer.echo(f"[🔍] Verwende Auto-Wordlist: {wordlist_name}")
            # Crackt den Hash für jede Wordlist und jeden Algorithmus
            for algo in algorithms_to_test:
                crack_hash(hash, wordlist_path, algo)
    else:
        # Standard-Wordlist oder benutzerdefinierte Wordlist verwenden
        wordlist_path = os.path.join("wordlist", wordlist_to_use)
        typer.echo(f"[🔍] Analysiere Hash: {hash} mit Wordlist: {wordlist_path} und Algorithmen: {', '.join(algorithms_to_test)}")
        for algo in algorithms_to_test:
            crack_hash(hash, wordlist_path, algo)
