import requests
from bs4 import BeautifulSoup

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")

konular = soup.select(".structItem--thread")

print(konular[7].prettify())
