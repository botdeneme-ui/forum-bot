import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Durum kodu:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

basliklar = soup.select(".structItem-title a")

print("Bulunan başlık sayısı:", len(basliklar))

for i, konu in enumerate(basliklar[:10], start=1):
    print(f"{i}. {konu.get_text(strip=True)}")
