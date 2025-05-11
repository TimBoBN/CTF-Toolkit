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

load_dotenv()  # Automatically loads the .env file

app = typer.Typer()

# Function to get subdomains from crt.sh
def get_subdomains_crtsh(domain: str):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        subdomains = set(entry["name_value"] for entry in data if "name_value" in entry)
        return sorted(list(subdomains))
    except Exception as e:
        return [f"Error with crt.sh: {e}"]

# Function to get Shodan data
def get_shodan_info(ip: str, api_key: str):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# Function to save data as JSON
def save_output_as_json(data: dict, filename_base: str):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    path = output_dir / f"{filename_base}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

# Function to extract title & meta information
def get_title_and_meta(soup):
    title = soup.title.string if soup.title else "No title found"
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

# Function to detect login forms
def detect_login_form(soup):
    forms = soup.find_all("form")
    for form in forms:
        if form.find("input", {"type": "password"}):
            return True
    return False

# Function to detect technologies
def detect_technologies(headers, soup):
    technologies = set()
    if "X-Powered-By" in headers and "PHP" in headers["X-Powered-By"]:
        technologies.add("PHP")
    if soup.find("script", {"src": lambda x: x and "jquery" in x.lower()}):
        technologies.add("jQuery")
    return list(technologies)

@app.command("scan")
def url_scan(url: str):
    """Scans a URL and extracts server info & web resources. Results are saved in the output/ folder (.json)."""
    typer.echo(f"[🌐] Starting scan: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        typer.echo(f"[❌] Error fetching the URL: {e}")
        raise typer.Exit()

    headers = response.headers
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Extract server info
    server_info = {
        "URL": url,
        "Status Code": response.status_code,
        "Server": headers.get("Server", "Unknown"),
        "X-Powered-By": headers.get("X-Powered-By", "Not specified"),
        "Content-Type": headers.get("Content-Type", "Unknown")
    }

    # Extract title and meta information
    title, meta = get_title_and_meta(soup)

    # Collect web resources
    resources = set()
    for tag in soup.find_all(["script", "link", "a"]):
        src = tag.get("src") or tag.get("href")
        if not src:
            continue
        if any(ext in src for ext in [".js", ".css", ".php"]):
            resources.add(src)

    # Login/Forms detection
    forms_detected = detect_login_form(soup)

    # Technology detection
    technologies = detect_technologies(headers, soup)

    # IP and subdomains
    parsed = urlparse(url)
    domain = parsed.netloc
    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        ip = "Unknown"

    subdomains = get_subdomains_crtsh(domain)

    # Shodan data
    shodan_key = os.getenv("SHODAN_API_KEY", "")
    shodan_data = get_shodan_info(ip, shodan_key) if (shodan_key and ip != "Unknown") else {"info": "Shodan scan not possible"}

    # Save JSON
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Timestamp without invalid characters
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
    typer.echo(f"[📦] JSON saved: {json_path}")

    # Output in terminal
    typer.echo(json.dumps(output_json, indent=2))

    typer.echo("[✅] Scan completed.")