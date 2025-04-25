import typer
from core.vulnscaner import scan_ports, detect_cms, basic_lfi_test, basic_sqli_test, basic_xss_test
import os
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

app = typer.Typer()

# Hole die Umgebungsvariablen aus der .env-Datei oder setze Standardwerte
default_url = os.getenv("DEFAULT_URL", "http://example.com")
default_target = os.getenv("DEFAULT_TARGET", "example.com")

@app.command()
def scan(
    target: str = typer.Option(default_target, "-t", "--target", help="Die IP oder Domain, die gescannt werden soll."),
    ports: str = typer.Option("1-1024", "-p", "--ports", help="Bereich der zu scannenden Ports (Standard: 1-1024)")
):
    """
    Scannt die offenen Ports eines Hosts mit Nmap.
    """
    scan_ports(target, ports)

@app.command()
def cms(url: str = typer.Option(default_url, "-u", "--url", help="Die URL der Website, die auf ein CMS überprüft werden soll.")):
    """
    Erkennt das CMS einer Website.
    """
    detect_cms(url)

@app.command()
def lfi(url: str = typer.Option(default_url, "-u", "--url", help="Die URL der Website, die auf LFI-Schwachstellen überprüft werden soll.")):
    """
    Führt grundlegende LFI-Tests durch.
    """
    basic_lfi_test(url)

@app.command()
def sqli(url: str = typer.Option(default_url, "-u", "--url", help="Die URL der Website, die auf SQLi-Schwachstellen überprüft werden soll.")):
    """
    Führt grundlegende SQLi-Tests durch.
    """
    basic_sqli_test(url)

@app.command()
def xss(url: str = typer.Option(default_url, "-u", "--url", help="Die URL der Website, die auf XSS-Schwachstellen überprüft werden soll.")):
    """
    Führt grundlegende XSS-Tests durch.
    """
    basic_xss_test(url)

if __name__ == "__main__":
    app()
