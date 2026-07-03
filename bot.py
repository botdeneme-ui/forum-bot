import os
import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"
BASE_URL = "https://forum.donanimarsivi.com"
LAST_FILE = "last_topic.txt"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/138 Safari/537.36"
    )
}

response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

konular = soup.select(".structItem--thread")

import re

en_buyuk_id = -1
hedef_link = None
hedef_baslik = None

for konu in konular:

    for a in konu.select(".structItem-title a"):

        href = a.get("href", "")

        if not href.startswith("/konu/"):
            continue

        eslesme = re.search(r"\.(\d+)/?$", href)

        if not eslesme:
            continue

        konu_id = int(eslesme.group(1))

        if konu_id > en_buyuk_id:
            en_buyuk_id = konu_id
            hedef_link = BASE_URL + href
            hedef_baslik = a.get_text(" ", strip=True)

if hedef_link is None:
    raise Exception("Konu bulunamadı.")

print("Takip edilen konu:")
print(hedef_baslik)
print("Konu ID:", en_buyuk_id)
print("Link:", hedef_link)

eski = ""

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        eski = f.read().strip()

# İlk çalıştırma
if eski == "":

    print("İlk çalıştırma.")

    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(str(en_buyuk_id))

    exit()

# Yeni konu var mı?
if eski != str(en_buyuk_id):

    mesaj = f"""🔥 Yeni Konu Açıldı!

📝 {hedef_baslik}

🔗 {hedef_link}
"""

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": mesaj,
            "disable_web_page_preview": True
        },
        timeout=20
    )

    print("Telegram bildirimi gönderildi.")

    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(str(en_buyuk_id))

else:

    print("Yeni konu yok.")
