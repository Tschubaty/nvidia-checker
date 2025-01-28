import requests
import hashlib

# Telegram API Credentials
BOT_TOKEN = "7952329988:AAFjIkeImVKVE9V6QfbWX-lPRDZ8U_VpG5w"
CHAT_ID = "674907506"

# URL to check
URL = "https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5090/"
CHECKSUM_FILE = "nvidia_checksum.txt"

def send_telegram_message(message):
    """Send a message to Telegram with the website link"""
    full_message = f"{message}\n🔗 [Check the website]({URL})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": full_message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def get_page_hash(url):
    """Fetch the webpage and compute a hash of its content."""
    response = requests.get(url)
    response.raise_for_status()
    return hashlib.md5(response.text.encode()).hexdigest()

def check_update():
    """Compare the current webpage content with the last saved version."""
    new_hash = get_page_hash(URL)

    try:
        with open(CHECKSUM_FILE, "r") as f:
            old_hash = f.read().strip()
    except FileNotFoundError:
        old_hash = ""

    if old_hash and old_hash != new_hash:
        send_telegram_message("🚀 The NVIDIA RTX 5090 page has been updated!")
        print("Website content changed!")

    with open(CHECKSUM_FILE, "w") as f:
        f.write(new_hash)

# Run the check once
check_update()
