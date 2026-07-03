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

hedef_baslik = None
hedef_link = None

for konu in konular:

    # Başlık bölümündeki bütün a etiketlerini al
    linkler = konu.select(".structItem-title a")

    # Gerçek konu linkini bul
    for a in linkler:

        href = a.get("href", "")

        if href.startswith("/konu/"):

            hedef_link = BASE_URL + href
            hedef_baslik = a.get_text(" ", strip=True)

            break

    # İlk gerçek konu bulundu
    if hedef_link:
        break

if hedef_link is None:
    raise Exception("Gerçek konu bulunamadı.")

print("Takip edilen konu:")
print(hedef_baslik)
print(hedef_link)

eski = ""

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        eski = f.read().strip()

# İlk çalıştırma
if eski == "":

    print("İlk çalıştırma.")

    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(hedef_link)

    exit()

# Yeni konu var mı?
if eski != hedef_link:

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
        f.write(hedef_link)

else:

    print("Yeni konu yok.")
