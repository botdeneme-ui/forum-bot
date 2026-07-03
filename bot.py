import os
import re
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

# Sayfayı indir
response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Konuları bul
konular = soup.select(".structItem--thread")

print("=" * 60)
print("Bulunan konu sayısı:", len(konular))
print("=" * 60)

for i, konu in enumerate(konular[:10], start=1):
    try:
        a = konu.select_one(".structItem-title a[href*='/konu/']")
        if a:
            print(f"{i}. {a.get_text(strip=True)}")
            print("   ", a["href"])
    except Exception as e:
        print(e)

# En büyük konu ID'sini bul
en_buyuk_id = -1
hedef_baslik = None
hedef_link = None

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
            hedef_baslik = a.get_text(" ", strip=True)
            hedef_link = BASE_URL + href

if hedef_link is None:
    raise Exception("Hiç konu bulunamadı!")

print("\nTakip edilen konu:")
print("Başlık :", hedef_baslik)
print("ID     :", en_buyuk_id)
print("Link   :", hedef_link)

# Eski ID oku
eski = ""

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        eski = f.read().strip()

# İlk çalıştırma
if eski == "":
    print("\nİlk çalıştırma.")

    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(str(en_buyuk_id))

    exit()

print("\nEski ID :", eski)
print("Yeni ID :", en_buyuk_id)

# Yeni konu kontrolü
if eski != str(en_buyuk_id):

    print("\n>>> YENİ KONU ALGILANDI <<<")

    mesaj = f"""🔥 Yeni Konu Açıldı!

📝 {hedef_baslik}

🔗 {hedef_link}
"""

    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": mesaj,
            "disable_web_page_preview": True
        },
        timeout=20
    )

    print("Telegram HTTP:", r.status_code)
    print("Telegram Cevabı:")
    print(r.text)

    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(str(en_buyuk_id))

    print("last_topic.txt güncellendi.")

else:

    print("\nYeni konu yok.")
