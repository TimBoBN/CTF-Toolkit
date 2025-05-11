import typer
from core.vulnscaner import scan_ports, detect_cms, basic_lfi_test, basic_sqli_test, basic_xss_test
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

app = typer.Typer()

# Get environment variables from the .env file or set default values
default_url = os.getenv("DEFAULT_URL", "http://example.com")
default_target = os.getenv("DEFAULT_TARGET", "example.com")

@app.command()
def scan(
    target: str = typer.Option(default_target, "-t", "--target", help="The IP or domain to be scanned."),
    ports: str = typer.Option("1-1024", "-p", "--ports", help="Range of ports to scan (default: 1-1024)")
):
    """
    Scans the open ports of a host using Nmap.
    """
    scan_ports(target, ports)

@app.command()
def cms(url: str = typer.Option(default_url, "-u", "--url", help="The URL of the website to check for a CMS.")):
    """
    Detects the CMS of a website.
    """
    detect_cms(url)

@app.command()
def lfi(url: str = typer.Option(default_url, "-u", "--url", help="The URL of the website to check for LFI vulnerabilities.")):
    """
    Performs basic LFI tests.
    """
    basic_lfi_test(url)

@app.command()
def sqli(url: str = typer.Option(default_url, "-u", "--url", help="The URL of the website to check for SQLi vulnerabilities.")):
    """
    Performs basic SQLi tests.
    """
    basic_sqli_test(url)

@app.command()
def xss(url: str = typer.Option(default_url, "-u", "--url", help="The URL of the website to check for XSS vulnerabilities.")):
    """
    Performs basic XSS tests.
    """
    basic_xss_test(url)

if __name__ == "__main__":
    app()