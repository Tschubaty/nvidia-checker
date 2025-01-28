import requests
import hashlib

# Telegram API-Zugangsdaten
BOT_TOKEN = "7952329988:AAFjIkeImVKVE9V6QfbWX-lPRDZ8U_VpG5w"
CHAT_ID = "674907506"

# Zu überprüfende Webseite
URL = "https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5090/"
CHECKSUM_FILE = "nvidia_checksum.txt"

def send_telegram_message(message):
    """Sendet eine Nachricht an Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_page_hash(url):
    """Lädt die Webseite und berechnet eine Hash-Summe vom Inhalt."""
    response = requests.get(url)
    response.raise_for_status()
    return hashlib.md5(response.text.encode()).hexdigest()

def check_update():
    """Vergleicht den aktuellen Inhalt mit der gespeicherten Version."""
    new_hash = get_page_hash(URL)

    try:
        with open(CHECKSUM_FILE, "r") as f:
            old_hash = f.read().strip()
    except FileNotFoundError:
        old_hash = ""

    if old_hash and old_hash != new_hash:
        send_telegram_message("🚀 Die NVIDIA RTX 5090 Seite wurde aktualisiert!")
        print("Webseite wurde geändert!")

    with open(CHECKSUM_FILE, "w") as f:
        f.write(new_hash)

# Einmal ausführen
check_update()
