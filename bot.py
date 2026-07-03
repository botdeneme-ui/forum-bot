import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")

konular = soup.select(".structItem--thread")

for i, konu in enumerate(konular[:10], 1):
    link = konu.select_one(".structItem-title a")

    print("=" * 40)
    print(i)
    print(link["href"])
