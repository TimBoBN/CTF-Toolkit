import requests
import whois
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import socket
import dns.resolver
import shodan
from dotenv import load_dotenv
import os

load_dotenv()
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
api = shodan.Shodan(SHODAN_API_KEY)


def get_subdomains(domain):
    print(f"[🌐] Suche Subdomains für: {domain} über crt.sh")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[❌] Fehler bei crt.sh: {response.status_code}")
            return []

        data = response.json()
        subdomains = set()

        for entry in data:
            name_value = entry.get("name_value")
            if name_value:
                for sub in name_value.split("\n"):
                    if sub.endswith(domain):
                        subdomains.add(sub.strip())

        return sorted(subdomains)

    except requests.exceptions.Timeout:
        print("[⚠️] Timeout beim Abrufen der Subdomains.")
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Anfragenfehler: {e}")
    except Exception as e:
        print(f"[⚠️] Fehler bei der Subdomain-Suche: {e}")
    return []

def get_whois_info(domain):
    print(f"[🧾] WHOIS-Abfrage für: {domain}")
    try:
        info = whois.whois(domain)
        if isinstance(info, dict):
            return {key: value for key, value in info.items()}
        else:
            print("[⚠️] WHOIS-Daten konnten nicht im erwarteten Format abgerufen werden.")
            return {}
    except whois.parser.PywhoisError:
        print("[⚠️] Fehler beim Verarbeiten der WHOIS-Daten.")
    except Exception as e:
        print(f"[⚠️] WHOIS-Abfrage fehlgeschlagen: {e}")
    return {}


def scrape_page(url):
    """
    Lädt den HTML-Inhalt der Seite herunter und durchsucht sie nach bestimmten Informationen.
    In diesem Fall suchen wir nach allen Links auf der Seite.
    """
    print(f"[🌐] Durchsuche die Seite: {url}")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[❌] Fehler beim Abrufen der Seite: {response.status_code}")
            return []

        # BeautifulSoup verwenden, um die Seite zu parsen
        soup = BeautifulSoup(response.text, 'html.parser')

        # Alle Links auf der Seite extrahieren
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Du kannst hier nach anderen Tags oder Inhalten suchen, z.B. <title>, <h1>, <p> usw.
        titles = soup.find_all(['h1', 'h2', 'h3', 'p'])

        print(f"[📄] Gefundene Links auf der Seite:")
        for link in links:
            print(link)

        print(f"[📄] Gefundene Titel und Absätze:")
        for title in titles:
            print(title.get_text(strip=True))

        return links

    except requests.exceptions.Timeout:
        print("[⚠️] Timeout beim Abrufen der Seite.")
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Anfragenfehler: {e}")
    except Exception as e:
        print(f"[⚠️] Fehler beim Scraping der Seite: {e}")
    return []


# DNS Resolver
def resolve_dns(domain):
    print(f"[🔍] DNS-Auflösung für: {domain}")
    records = {}
    try:
        # A-Records
        a_records = dns.resolver.resolve(domain, 'A')
        records['A'] = [ip.address for ip in a_records]
        
        # AAAA-Records
        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            records['AAAA'] = [ip.address for ip in aaaa_records]
        except dns.resolver.NoAnswer:
            records['AAAA'] = []
        
        # MX-Records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            records['MX'] = [mx.exchange.to_text() for mx in mx_records]
        except dns.resolver.NoAnswer:
            records['MX'] = []
        
        # TXT-Records
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            records['TXT'] = [txt.to_text() for txt in txt_records]
        except dns.resolver.NoAnswer:
            records['TXT'] = []
        
        return records
    except Exception as e:
        print(f"[⚠️] Fehler bei der DNS-Auflösung: {e}")
        return {}

# Portscanner (Verwenden von socket)
def port_scan(domain, start_port=1, end_port=1024):
    print(f"[🔐] Scanne Ports für: {domain}")
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    return open_ports

# Robots.txt und Header
def get_robots_txt(url):
    robots_url = url + "/robots.txt"
    print(f"[📄] Abrufen der robots.txt für: {robots_url}")
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[⚠️] Keine robots.txt gefunden oder Fehler: {response.status_code}")
    except Exception as e:
        print(f"[⚠️] Fehler beim Abrufen der robots.txt: {e}")
    return ""

def get_headers(url):
    print(f"[🔑] Abrufen der HTTP-Header für: {url}")
    try:
        response = requests.head(url, timeout=10)
        return response.headers
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Fehler beim Abrufen der Header: {e}")
    return {}

def get_technologies(url):
    print(f"[🛠️] Technologien auf der Seite erkennen: {url}")
    try:
        response = requests.get(url, timeout=10)
        # Beispiel: Überprüfung auf bekannte Technologien anhand von HTTP-Headern
        technologies = {}
        if 'X-Powered-By' in response.headers:
            technologies['X-Powered-By'] = response.headers['X-Powered-By']
        if 'Server' in response.headers:
            technologies['Server'] = response.headers['Server']
        return technologies
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Fehler beim Erkennen der Technologien: {e}")
    return {}

# Shodan-Integration
def shodan_info(ip_or_domain):
    print(f"[🔎] Abrufen von Shodan-Informationen für: {ip_or_domain}")
    try:
        result = api.host(ip_or_domain)
        return result
    except shodan.APIError as e:
        print(f"[⚠️] Fehler bei der Shodan-Abfrage: {e}")
    return {}