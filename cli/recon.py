import typer
from core import recon  # Importiere die Funktionen aus core.recon
from core.recon import scrape_page  # Neue Funktion für das Scraping

app = typer.Typer()

@app.command("subdomains")
def subdomains(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    typer.echo(f"\n[📋] Suche nach Subdomains für: {domain}")
    subs = recon.get_subdomains(domain)
    if subs:
        typer.echo(f"\n[📋] Gefundene Subdomains:")
        for sub in subs:
            typer.echo(f"- {sub}")
    else:
        typer.echo("[❌] Keine Subdomains gefunden oder ein Fehler trat auf.")

@app.command("whoisinfo")
def whoisinfo(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    typer.echo(f"\n[📄] WHOIS-Daten für: {domain}\n")
    info = recon.get_whois_info(domain)
    if info:
        for key, value in info.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] Fehler beim Abrufen der WHOIS-Daten.")

@app.command("scrape")
def scrape(domain: str):
    # Hier gehen wir davon aus, dass du die Subdomains bereits abgerufen hast und die Seiten durchsuchst
    subdomains = recon.get_subdomains(domain)
    if subdomains:
        for sub in subdomains:
            # Wir durchsuchen jede Subdomain
            print(f"\n[🌐] Durchsuche Subdomain: {sub}")
            recon.scrape_page(f"http://{sub}")  # Du kannst auch "https://" verwenden, wenn das erforderlich ist
    else:
        print("[❌] Keine Subdomains gefunden.")

@app.command("dns")
def dns(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    typer.echo(f"\n[🔍] DNS-Auflösung für: {domain}")
    records = recon.resolve_dns(domain)
    if records:
        for record_type, record_list in records.items():
            typer.echo(f"\n[📋] {record_type} Records:")
            for record in record_list:
                typer.echo(f"- {record}")
    else:
        typer.echo("[❌] Keine DNS-Daten gefunden.")

@app.command("portscan")
def portscan(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    typer.echo(f"\n[🔐] Scanne Ports für: {domain}")
    open_ports = recon.port_scan(domain)
    if open_ports:
        typer.echo(f"\n[📋] Gefundene offene Ports:")
        for port in open_ports:
            typer.echo(f"- {port}")
    else:
        typer.echo("[❌] Keine offenen Ports gefunden.")

@app.command("robots")
def robots(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    url = f"http://{domain}"
    typer.echo(f"\n[📄] Abrufe robots.txt für: {url}")
    robots_txt = recon.get_robots_txt(url)
    if robots_txt:
        typer.echo(f"\n[📋] Inhalt der robots.txt:\n{robots_txt}")
    else:
        typer.echo("[❌] Keine robots.txt gefunden.")

@app.command("headers")
def headers(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    url = f"http://{domain}"
    typer.echo(f"\n[🔑] Abrufe HTTP-Header für: {url}")
    headers = recon.get_headers(url)
    if headers:
        for key, value in headers.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] Fehler beim Abrufen der HTTP-Header.")

@app.command("technologies")
def technologies(domain: str):
    if not domain:
        typer.echo("Bitte gib eine gültige Domain ein.")
        return

    url = f"http://{domain}"
    typer.echo(f"\n[🛠️] Erkenne Technologien für: {url}")
    tech = recon.get_technologies(url)
    if tech:
        for key, value in tech.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] Keine Technologien erkannt.")

@app.command("shodan")
def shodan_info_cmd(ip_or_domain: str):
    if not ip_or_domain:
        typer.echo("Bitte gib eine gültige IP oder Domain ein.")
        return

    typer.echo(f"\n[🔎] Abrufen von Shodan-Informationen für: {ip_or_domain}")
    result = recon.shodan_info(ip_or_domain)
    if result:
        typer.echo(f"[📋] Shodan-Informationen:")
        for key, value in result.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] Keine Shodan-Informationen gefunden.")
