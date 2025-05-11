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
    print(f"[🌐] Searching for subdomains for: {domain} via crt.sh")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[❌] Error with crt.sh: {response.status_code}")
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
        print("[⚠️] Timeout while fetching subdomains.")
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Request error: {e}")
    except Exception as e:
        print(f"[⚠️] Error during subdomain search: {e}")
    return []

def get_whois_info(domain):
    print(f"[🧾] WHOIS query for: {domain}")
    try:
        info = whois.whois(domain)
        if isinstance(info, dict):
            return {key: value for key, value in info.items()}
        else:
            print("[⚠️] WHOIS data could not be retrieved in the expected format.")
            return {}
    except whois.parser.PywhoisError:
        print("[⚠️] Error processing WHOIS data.")
    except Exception as e:
        print(f"[⚠️] WHOIS query failed: {e}")
    return {}


def scrape_page(url):
    """
    Downloads the HTML content of the page and searches for specific information.
    In this case, we are looking for all links on the page.
    """
    print(f"[🌐] Scraping the page: {url}")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[❌] Error fetching the page: {response.status_code}")
            return []

        # Use BeautifulSoup to parse the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all links on the page
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # You can search for other tags or content here, e.g., <title>, <h1>, <p>, etc.
        titles = soup.find_all(['h1', 'h2', 'h3', 'p'])

        print(f"[📄] Links found on the page:")
        for link in links:
            print(link)

        print(f"[📄] Titles and paragraphs found:")
        for title in titles:
            print(title.get_text(strip=True))

        return links

    except requests.exceptions.Timeout:
        print("[⚠️] Timeout while fetching the page.")
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Request error: {e}")
    except Exception as e:
        print(f"[⚠️] Error scraping the page: {e}")
    return []


# DNS Resolver
def resolve_dns(domain):
    print(f"[🔍] Resolving DNS for: {domain}")
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
        print(f"[⚠️] Error during DNS resolution: {e}")
        return {}

# Portscanner (Using socket)
def port_scan(domain, start_port=1, end_port=1024):
    print(f"[🔐] Scanning ports for: {domain}")
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    return open_ports

# Robots.txt and Header
def get_robots_txt(url):
    robots_url = url + "/robots.txt"
    print(f"[📄] Fetching robots.txt for: {robots_url}")
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[⚠️] No robots.txt found or error: {response.status_code}")
    except Exception as e:
        print(f"[⚠️] Error fetching robots.txt: {e}")
    return ""

def get_headers(url):
    print(f"[🔑] Fetching HTTP headers for: {url}")
    try:
        response = requests.head(url, timeout=10)
        return response.headers
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Error fetching headers: {e}")
    return {}

def get_technologies(url):
    print(f"[🛠️] Detecting technologies on the page: {url}")
    try:
        response = requests.get(url, timeout=10)
        # Example: Check for known technologies based on HTTP headers
        technologies = {}
        if 'X-Powered-By' in response.headers:
            technologies['X-Powered-By'] = response.headers['X-Powered-By']
        if 'Server' in response.headers:
            technologies['Server'] = response.headers['Server']
        return technologies
    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Error detecting technologies: {e}")
    return {}

# Shodan Integration
def shodan_info(ip_or_domain):
    print(f"[🔎] Fetching Shodan information for: {ip_or_domain}")
    try:
        result = api.host(ip_or_domain)
        return result
    except shodan.APIError as e:
        print(f"[⚠️] Error during Shodan query: {e}")
    return {}