from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

URL = "https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get(URL)

    time.sleep(5)

    print("Sayfa başlığı:")
    print(driver.title)

    print("-------------------")

    print(driver.page_source[:3000])

finally:
    driver.quit()
