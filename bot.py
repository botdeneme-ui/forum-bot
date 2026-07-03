import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

konular = soup.select(".structItem--thread")

print("Toplam konu:", len(konular))

for i, konu in enumerate(konular[:8], start=1):
    print("=" * 50)
    print("Sıra:", i)
    print("CLASS:", konu.get("class"))
    print("HTML:")
    print(str(konu)[:1500])   # İlk 1500 karakterini yazdır
