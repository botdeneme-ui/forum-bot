import os
import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"
BASE = "https://forum.donanimarsivi.com"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

konular = soup.select(".structItem--thread")

# İlk normal konu (ilk 7 kayıt sabit)
konu = konular[7]

# İkinci <a> etiketi gerçek konu linkidir
link = konu.select(".structItem-title a")[1]

baslik = link.get_text(strip=True)
url = BASE + link["href"]

print("Takip edilen konu:", baslik)

DOSYA = "last_topic.txt"

if os.path.exists(DOSYA):
    with open(DOSYA, "r", encoding="utf-8") as f:
        eski = f.read().strip()
else:
    eski = ""

if eski == "":
    print("İlk çalıştırma")

elif eski != url:

    mesaj = f"""🔥 Yeni Konu!

📝 {baslik}

🔗 {url}
"""

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": mesaj,
            "disable_web_page_preview": True
        }
    )

    print("Telegram bildirimi gönderildi.")

with open(DOSYA, "w", encoding="utf-8") as f:
    f.write(url)
