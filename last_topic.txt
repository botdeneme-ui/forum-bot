import os
import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

konular = soup.select(".structItem--thread")

if len(konular) < 5:
    raise Exception("Yeterli konu bulunamadı.")

# İlk 4 sabit konuyu geç
konu = konular[4]

baslik = konu.select_one(".structItem-title a").get_text(strip=True)
link = "https://forum.donanimarsivi.com" + konu.select_one(".structItem-title a")["href"]

print("Takip edilen konu:", baslik)

DOSYA = "last_topic.txt"

if os.path.exists(DOSYA):
    with open(DOSYA, "r", encoding="utf-8") as f:
        eski = f.read().strip()
else:
    eski = ""

if eski == "":
    print("İlk çalıştırma.")
    with open(DOSYA, "w", encoding="utf-8") as f:
        f.write(baslik)

elif eski != baslik:

    mesaj = f"""🔥 Yeni Konu Açıldı!

{baslik}

{link}
"""

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": mesaj
        }
    )

    print("Telegram bildirimi gönderildi.")

    with open(DOSYA, "w", encoding="utf-8") as f:
        f.write(baslik)

else:
    print("Yeni konu yok.")
