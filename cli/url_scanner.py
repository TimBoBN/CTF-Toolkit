import typer
import os
import json
import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()  # Lädt die .env-Datei automatisch

app = typer.Typer()

# Funktion, um Subdomains von crt.sh zu bekommen
def get_subdomains_crtsh(domain: str):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        subdomains = set(entry["name_value"] for entry in data if "name_value" in entry)
        return sorted(list(subdomains))
    except Exception as e:
        return [f"Fehler bei crt.sh: {e}"]

# Funktion, um Shodan-Daten zu erhalten
def get_shodan_info(ip: str, api_key: str):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# Funktion, um Daten als JSON zu speichern
def save_output_as_json(data: dict, filename_base: str):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    path = output_dir / f"{filename_base}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

# Funktion, um den Title & Meta-Infos zu extrahieren
def get_title_and_meta(soup):
    title = soup.title.string if soup.title else "Kein Titel gefunden"
    meta = {
        "description": None,
        "keywords": None
    }
    for tag in soup.find_all("meta"):
        if tag.get("name") == "description":
            meta["description"] = tag.get("content")
        elif tag.get("name") == "keywords":
            meta["keywords"] = tag.get("content")
    return title, meta


# Funktion, um Formular zu erkennen
def detect_login_form(soup):
    forms = soup.find_all("form")
    for form in forms:
        if form.find("input", {"type": "password"}):
            return True
    return False

# Funktion, um Technologie zu erkennen
def detect_technologies(headers, soup):
    technologies = set()
    if "X-Powered-By" in headers and "PHP" in headers["X-Powered-By"]:
        technologies.add("PHP")
    if soup.find("script", {"src": lambda x: x and "jquery" in x.lower()}):
        technologies.add("jQuery")
    return list(technologies)

@app.command("scan")
def url_scan(url: str):
    """Scannt eine URL und extrahiert Serverinfos & Webressourcen. Ergebnisse werden im output/-Ordner gespeichert (.json)"""
    typer.echo(f"[🌐] Starte Scan: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        typer.echo(f"[❌] Fehler beim Abrufen der URL: {e}")
        raise typer.Exit()

    headers = response.headers
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Serverinfos extrahieren
    server_info = {
        "URL": url,
        "Status-Code": response.status_code,
        "Server": headers.get("Server", "Unbekannt"),
        "X-Powered-By": headers.get("X-Powered-By", "Nicht angegeben"),
        "Content-Type": headers.get("Content-Type", "Unbekannt")
    }

    # Title und Meta-Infos extrahieren
    title, meta = get_title_and_meta(soup)

    # Webressourcen sammeln
    resources = set()
    for tag in soup.find_all(["script", "link", "a"]):
        src = tag.get("src") or tag.get("href")
        if not src:
            continue
        if any(ext in src for ext in [".js", ".css", ".php"]):
            resources.add(src)



    # Login/Forms Detection
    forms_detected = detect_login_form(soup)

    # Technologie-Erkennung
    technologies = detect_technologies(headers, soup)

    # IP und Subdomains
    parsed = urlparse(url)
    domain = parsed.netloc
    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        ip = "Unbekannt"

    subdomains = get_subdomains_crtsh(domain)

    # Shodan-Daten
    shodan_key = os.getenv("SHODAN_API_KEY", "")
    shodan_data = get_shodan_info(ip, shodan_key) if (shodan_key and ip != "Unbekannt") else {"info": "Kein Shodan-Scan möglich"}

    # JSON speichern
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Timestamp ohne ungültige Zeichen
    output_json = {
        "domain": domain,
        "ip": ip,
        "server_info": server_info,
        "title": title,
        "meta": meta,
        "resources": sorted(list(resources)),
        "subdomains_crtsh": subdomains,
        "shodan_data": shodan_data,
        "forms_detected": forms_detected,
        "technologies": technologies,
        "scan_time": timestamp,
        "sitemap": url + "/sitemap.xml",
        "robots.txt": url + "/robots.txt"
    }

    json_path = save_output_as_json(output_json, f"{domain}_{timestamp}")
    typer.echo(f"[📦] JSON gespeichert: {json_path}")

    # Ausgabe im Terminal
    typer.echo(json.dumps(output_json, indent=2))

    typer.echo("[✅] Scan abgeschlossen.")
