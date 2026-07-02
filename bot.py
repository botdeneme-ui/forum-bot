import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

basliklar = soup.select(".structItem-title a")

if not basliklar:
    print("Konu bulunamadı.")
    exit()

ilk_konu = basliklar[0]

print("Başlık :", ilk_konu.get_text(strip=True))

link = ilk_konu.get("href", "")

if link.startswith("/"):
    link = "https://forum.donanimarsivi.com" + link

print("Link    :", link)
