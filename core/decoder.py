import base64
from urllib.parse import unquote
import html


def decode_base64(s: str) -> str | None:
    try:
        return base64.b64decode(s).decode()
    except:
        return None


def decode_base32(s: str) -> str | None:
    try:
        return base64.b32decode(s).decode()
    except:
        return None


def decode_base85(s: str) -> str | None:
    try:
        return base64.b85decode(s).decode()
    except:
        return None


def decode_hex(s: str) -> str | None:
    try:
        return bytes.fromhex(s).decode()
    except:
        return None


def decode_rot13(s: str) -> str | None:
    try:
        return s.translate(str.maketrans(
            "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
            "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
        ))
    except:
        return None


def decode_url(s: str) -> str | None:
    try:
        return unquote(s)
    except:
        return None


def decode_html(s: str) -> str | None:
    try:
        return html.unescape(s)
    except:
        return None


def decode_binary(s: str) -> str | None:
    try:
        return ''.join([chr(int(b, 2)) for b in s.split()])
    except:
        return None


def decode_morse(s: str) -> str | None:
    morse_code_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D',
        '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
        '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
        '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1',
        '..---': '2', '...--': '3', '....-': '4', '.....': '5',
        '-....': '6', '--...': '7', '---..': '8', '----.': '9'
    }
    try:
        words = s.strip().split(" / ")
        decoded = ""
        for word in words:
            for char in word.split():
                decoded += morse_code_dict.get(char, '?')
            decoded += ' '
        return decoded.strip()
    except:
        return None


# ✅ Decoder map for auto-scan

decoders = {
    "Base64": decode_base64,
    "Base32": decode_base32,
    "Base85": decode_base85,
    "Hex": decode_hex,
    "ROT13": decode_rot13,
    "URL": decode_url,
    "HTML": decode_html,
    "Binary": decode_binary,
    "Morse": decode_morse,
}
