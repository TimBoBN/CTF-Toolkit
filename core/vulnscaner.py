import nmap
import requests
from urllib.parse import urljoin
import re

def scan_ports(target: str, ports: str = "1-1024") -> None:
    """
    Scans open ports on a target host using Nmap.
    :param target: Target host (IP or domain)
    :param ports: Range of ports to scan (default: 1-1024)
    """
    nm = nmap.PortScanner()
    print(f"[🔍] Scanning ports for {target} on ports: {ports}...")

    try:
        nm.scan(target, ports)
        for host in nm.all_hosts():
            print(f"[🌐] Host: {host} ({nm[host].hostname()})")
            for proto in nm[host].all_protocols():
                print(f"  Protocol: {proto}")
                lport = nm[host][proto].keys()
                for port in lport:
                    state = nm[host][proto][port]["state"]
                    print(f"    Port: {port} - Status: {state}")
    except Exception as e:
        print(f"[⚠️] Error scanning {target}: {e}")

def detect_cms(url: str) -> None:
    """
    Detects the CMS of a website based on headers and meta tags.
    :param url: URL of the website to scan
    """
    try:
        response = requests.get(url)
        cms = None

        # Check headers for known CMS identifiers
        if 'X-Powered-By' in response.headers:
            if 'WordPress' in response.headers['X-Powered-By']:
                cms = 'WordPress'
            elif 'Joomla' in response.headers['X-Powered-By']:
                cms = 'Joomla'
        
        # Check meta tags for CMS-specific information
        if not cms and 'content' in response.text:
            if "wp-content" in response.text:
                cms = 'WordPress'
            elif "joomla" in response.text:
                cms = 'Joomla'

        if cms:
            print(f"[📋] Detected CMS: {cms}")
        else:
            print("[⚠️] No CMS detected.")
    
    except requests.RequestException as e:
        print(f"[⚠️] Error fetching the website: {e}")

def basic_lfi_test(url: str) -> None:
    """
    Tests a website for basic LFI vulnerabilities.
    :param url: The URL to test
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
                print(f"[⚠️] LFI vulnerability found at {test_url}")
        except requests.RequestException:
            pass

def basic_sqli_test(url: str) -> None:
    """
    Tests a website for basic SQLi vulnerabilities.
    :param url: The URL to test
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
                print(f"[⚠️] SQLi vulnerability found at {test_url}")
        except requests.RequestException:
            pass

def basic_xss_test(url: str) -> None:
    """
    Tests a website for basic XSS vulnerabilities.
    :param url: The URL to test
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
                print(f"[⚠️] XSS vulnerability found at {test_url}")
        except requests.RequestException:
            pass