import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

try:
    response = requests.get(URL, headers=headers, timeout=20)
    response.raise_for_status()
except Exception as e:
    print("Forum okunamadı:", e)
    raise

soup = BeautifulSoup(response.text, "html.parser")

konular = soup.select(".structItem--thread")

print("=" * 60)
print("Bulunan konu sayısı:", len(konular))
print("=" * 60)

tum_konular = []

for konu in konular:

    for a in konu.select(".structItem-title a"):

        href = a.get("href", "")

        if not href.startswith("/konu/"):
            continue

        m = re.search(r"\.(\d+)/?$", href)

        if not m:
            continue

        konu_id = int(m.group(1))

        tum_konular.append({
            "id": konu_id,
            "baslik": a.get_text(" ", strip=True),
            "link": BASE_URL + href
        })

        break

tum_konular.sort(key=lambda x: x["id"])

print("Okunan konu ID'leri:")

for konu in tum_konular[-10:]:
    print(konu["id"], "-", konu["baslik"])

eski = 0

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        veri = f.read().strip()
        if veri.isdigit():
            eski = int(veri)

print("\nSon kayıtlı ID :", eski)

# İlk çalıştırma
if eski == 0:

    son = tum_konular[-1]["id"]

    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(str(son))

    print("İlk çalıştırma. Son ID kaydedildi:", son)
    exit()

yeni_konular = [k for k in tum_konular if k["id"] > eski]

print("Yeni konu sayısı:", len(yeni_konular))

if not yeni_konular:
    print("Yeni konu yok.")
    exit()

for konu in yeni_konular:

    mesaj = (
        "🔥 <b>Yeni Konu Açıldı!</b>\n\n"
        f"📝 <b>{konu['baslik']}</b>\n\n"
        f"🆔 {konu['id']}\n\n"
        f"🔗 {konu['link']}\n\n"
        f"🕒 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    )

    try:
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": mesaj,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=20
        )

        print(f"{konu['id']} gönderildi -> {r.status_code}")

        if r.status_code != 200:
            print(r.text)

    except Exception as e:
        print("Telegram hatası:", e)

son_id = max(k["id"] for k in tum_konular)

with open(LAST_FILE, "w", encoding="utf-8") as f:
    f.write(str(son_id))

print("\nlast_topic.txt güncellendi:", son_id)
