import typer
import os
from core.cracker import crack_hash
import hashlib
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = typer.Typer()

# Get environment variables or set defaults
default_algorithm = os.getenv("DEFAULT_ALGORITHM", "auto")
default_wordlist = os.getenv("DEFAULT_WORDLIST", "rockyou.txt")
auto_wordlist_dir = os.getenv("AUTO_WORDLIST_DIR", "auto_wordlists")  # Folder for auto wordlists

@app.command()
def hash(
    hash: str,
    wordlist: str = typer.Option(None, "-w", "--wordlist", help="Wordlist to use. If not provided, the default or auto wordlist will be used."),
    algorithm: str = typer.Option(default_algorithm, "-a", "--algorithm", help="Hash algorithm to use. If 'auto', all supported algorithms will be tried.")
):
    """
    Cracks a hash against a wordlist using a specified or all supported hash algorithms.
    """
    if algorithm == "auto":
        algorithms_to_test = hashlib.algorithms_guaranteed
        typer.echo("[🔍] Trying all supported algorithms: " + ", ".join(algorithms_to_test))
        
        # Load all wordlists in the auto folder
        wordlist_files = [f for f in os.listdir(auto_wordlist_dir) if os.path.isfile(os.path.join(auto_wordlist_dir, f))]
        
        if not wordlist_files:
            typer.echo(f"[⚠️] No wordlists found in auto folder: {auto_wordlist_dir}")
            return
        
        typer.echo(f"[🔍] Using auto wordlists from folder: {auto_wordlist_dir}")
    elif algorithm:
        algorithms_to_test = [algorithm]
        typer.echo(f"[🔍] Only algorithm {algorithm} will be tested.")
        wordlist_to_use = wordlist if wordlist else default_wordlist
        typer.echo(f"[🔍] Using wordlist: {wordlist_to_use}")
    else:
        algorithms_to_test = hashlib.algorithms_guaranteed
        typer.echo("[🔍] Trying all supported algorithms.")
        wordlist_to_use = wordlist if wordlist else default_wordlist

    # Use wordlists from folder in auto mode
    if algorithm == "auto":
        for wordlist_name in wordlist_files:
            wordlist_path = os.path.join(auto_wordlist_dir, wordlist_name)
            typer.echo(f"[🔍] Using auto wordlist: {wordlist_name}")
            for algo in algorithms_to_test:
                crack_hash(hash, wordlist_path, algo)
    else:
        wordlist_path = os.path.join("wordlist", wordlist_to_use)
        typer.echo(f"[🔍] Analyzing hash: {hash} using wordlist: {wordlist_path} and algorithms: {', '.join(algorithms_to_test)}")
        for algo in algorithms_to_test:
            crack_hash(hash, wordlist_path, algo)
