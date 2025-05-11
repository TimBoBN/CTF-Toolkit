import typer
from core import recon  # Import functions from core.recon
from core.recon import scrape_page  # New function for scraping

app = typer.Typer()

@app.command("subdomains")
def subdomains(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    typer.echo(f"\n[📋] Searching for subdomains of: {domain}")
    subs = recon.get_subdomains(domain)
    if subs:
        typer.echo(f"\n[📋] Found subdomains:")
        for sub in subs:
            typer.echo(f"- {sub}")
    else:
        typer.echo("[❌] No subdomains found or an error occurred.")

@app.command("whoisinfo")
def whoisinfo(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    typer.echo(f"\n[📄] WHOIS data for: {domain}\n")
    info = recon.get_whois_info(domain)
    if info:
        for key, value in info.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] Error fetching WHOIS data.")

@app.command("scrape")
def scrape(domain: str):
    # Here, we assume you've already retrieved the subdomains and are scraping the pages
    subdomains = recon.get_subdomains(domain)
    if subdomains:
        for sub in subdomains:
            # Scraping each subdomain
            print(f"\n[🌐] Scraping subdomain: {sub}")
            recon.scrape_page(f"http://{sub}")  # You can also use "https://" if necessary
    else:
        print("[❌] No subdomains found.")

@app.command("dns")
def dns(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    typer.echo(f"\n[🔍] DNS resolution for: {domain}")
    records = recon.resolve_dns(domain)
    if records:
        for record_type, record_list in records.items():
            typer.echo(f"\n[📋] {record_type} records:")
            for record in record_list:
                typer.echo(f"- {record}")
    else:
        typer.echo("[❌] No DNS data found.")

@app.command("portscan")
def portscan(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    typer.echo(f"\n[🔐] Scanning ports for: {domain}")
    open_ports = recon.port_scan(domain)
    if open_ports:
        typer.echo(f"\n[📋] Found open ports:")
        for port in open_ports:
            typer.echo(f"- {port}")
    else:
        typer.echo("[❌] No open ports found.")

@app.command("robots")
def robots(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    url = f"http://{domain}"
    typer.echo(f"\n[📄] Fetching robots.txt for: {url}")
    robots_txt = recon.get_robots_txt(url)
    if robots_txt:
        typer.echo(f"\n[📋] robots.txt content:\n{robots_txt}")
    else:
        typer.echo("[❌] No robots.txt found.")

@app.command("headers")
def headers(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    url = f"http://{domain}"
    typer.echo(f"\n[🔑] Fetching HTTP headers for: {url}")
    headers = recon.get_headers(url)
    if headers:
        for key, value in headers.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] Error fetching HTTP headers.")

@app.command("technologies")
def technologies(domain: str):
    if not domain:
        typer.echo("Please enter a valid domain.")
        return

    url = f"http://{domain}"
    typer.echo(f"\n[🛠️] Detecting technologies for: {url}")
    tech = recon.get_technologies(url)
    if tech:
        for key, value in tech.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] No technologies detected.")

@app.command("shodan")
def shodan_info_cmd(ip_or_domain: str):
    if not ip_or_domain:
        typer.echo("Please enter a valid IP or domain.")
        return

    typer.echo(f"\n[🔎] Fetching Shodan information for: {ip_or_domain}")
    result = recon.shodan_info(ip_or_domain)
    if result:
        typer.echo(f"[📋] Shodan information:")
        for key, value in result.items():
            typer.echo(f"{key}: {value}")
    else:
        typer.echo("[❌] No Shodan information found.")
