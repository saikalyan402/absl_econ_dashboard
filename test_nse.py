import asyncio
from scraper_jobs import URLS
from scraper_core import get_selenium_driver
from bs4 import BeautifulSoup
import time

url = URLS["high_low_52weeks"]

driver = get_selenium_driver()
try:
    print(f"Loading {url}")
    driver.get(url)
    time.sleep(8)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables.")
    if tables:
        for i, t in enumerate(tables):
            print(f"Table {i} has {len(t.find_all('tr'))} rows")
    else:
        print("No tables found. Page source snippet:")
        print(driver.page_source[:1000])
        driver.save_screenshot("nse_error.png")
finally:
    driver.quit()



