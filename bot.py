from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get(URL)

    basliklar = driver.find_elements(By.CSS_SELECTOR, ".structItem-title a")

    print("Bulunan konular:")
    print("-" * 40)

    for i, baslik in enumerate(basliklar[:10], start=1):
        print(f"{i}. {baslik.text}")

finally:
    driver.quit()
