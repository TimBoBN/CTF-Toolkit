
# 🛠️ CTF Toolkit

A modular CLI toolkit for CTFs, Pentesting, and Red Teaming – focused on automation, reconnaissance, exploitation, and analysis. Developed for fast, locally executable tests without unnecessary dependencies.

## ⚙️ Features

- **Cracking**
  - Hash cracking with wordlists (e.g., MD5, SHA1, SHA256, ...)
- **Decoder**
  - Base64, Hex, URL, JS-Unicode, ROT13, Morse, Binary, Auto-Test
- **Regex Toolkit**
  - Pattern search using regular expressions
- **Hashing**
  - Hash arbitrary text (md5, sha1, sha256, …)
- **Reconnaissance**
  - Subdomain Finder, WHOIS, Scraping, DNS Info, Portscan, Header Check, Shodan
- **Vulnerability Scanning**
  - LFI Check, CMS Detection, basic SQLi analysis
- **Output**
  - Results can optionally be saved in `output/` with date/URL

---

## 🚀 Examples

### 🔓 Hash Cracking

```bash
python main.py crack hash <HASH> <WORDLIST> -a/--algorithm <ALGO>
python main.py crack hash 5f4dcc3b5aa765d61d8327deb882cf99 rockyou.txt -a md5
```

### 🔐 Hash Creation

```bash
python main.py hash create <TEXT> [--algo <ALGORITHM>]
python main.py hash create secret --algo sha256
```

### 🧪 Decoder

```bash
python main.py decode run base64 aGVsbG8gd29ybGQ=
python main.py decode run hex 48656c6c6f
python main.py decode run url hallo%20welt
python main.py decode run js Hi
python main.py decode run rot13 Uryyb
python main.py decode run binary 01001000 01101001
python main.py decode run morse .... . .-.. .-.. --- / .-- --- .-. .-.. -..
python main.py decode run test <TEXT>  # Automatic decoder detection
```

### 🔎 Regex Search

```bash
python main.py regex search "\d{4,}" "The number is 1234 in the year 2025"
```

### 🌐 Reconnaissance

```bash
python main.py recon subdomains example.com
python main.py recon whoisinfo example.com
python main.py recon scrape example.com
python main.py recon portscan example.com
python main.py recon dns example.com
python main.py recon headers example.com
python main.py recon robots example.com
python main.py recon shodan example.com
python main.py recon technologies example.com
```

### 🛡️ Vulnerability Scanning

```bash
python main.py vulnscan scan -t example.com -p 1-1024         # Portscan
python main.py vulnscan cms -u http://example.com            # CMS Detection
python main.py vulnscan lfi -u http://example.com/index.php?file=
python main.py sqli -u http://example.com/item.php           # Basic SQLi check
```

---

## 🧰 Project Structure

```
ctf-toolkit/
├── main.py
├── modules/
│   ├── crack/
│   ├── decode/
│   ├── hash/
│   ├── regex/
│   ├── recon/
│   └── vulnscan/
├── utils/
├── output/
└── requirements.txt
```

---

## 📦 Installation

```bash
git clone https://github.com/timbobn/ctf-toolkit.git
cd ctf-toolkit
pip install -r requirements.txt
```

> Requires Python 3.9+ and possibly an API key for Shodan (if used)

---

## 📜 License

MIT License – free to use for education, research, and personal purposes.

---

## 🤝 Contribute

Pull requests, bug reports, and new modules are welcome! Simply create an issue or fork the repo.
