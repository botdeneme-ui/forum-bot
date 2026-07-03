import os
import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"
BASE_URL = "https://forum.donanimarsivi.com"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

konular = soup.select(".structItem--thread")

ilk_normal = None

for konu in konular:
    # Sabit konuları atla
    if "structItem--sticky" in konu.get("class", []):
        continue

    ilk_normal = konu
    break

if ilk_normal is None:
    raise Exception("Normal konu bulunamadı.")

link_eleman = ilk_normal.select_one(".structItem-title a")

baslik = link_eleman.get_text(strip=True)
link = BASE_URL + link_eleman["href"]

print("Takip edilen konu:", baslik)

DOSYA = "last_topic.txt"

if os.path.exists(DOSYA):
    with open(DOSYA, "r", encoding="utf-8") as f:
        eski = f.read().strip()
else:
    eski = ""

if eski == "":
    print("İlk çalıştırma")
    with open(DOSYA, "w", encoding="utf-8") as f:
        f.write(link)

elif eski != link:

    mesaj = f"""🔥 Yeni Konu Açıldı

📝 {baslik}

🔗 {link}
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

    with open(DOSYA, "w", encoding="utf-8") as f:
        f.write(link)

else:
    print("Yeni konu yok.")
