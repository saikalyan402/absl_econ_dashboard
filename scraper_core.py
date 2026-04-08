import httpx
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

def get_selenium_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)
    return driver

async def fetch_with_bs4_and_fallback(url: str, parse_func):
    """
    Attempts to fetch `url` with httpx, parses HTML via soup and passes to `parse_func`.
    If failed or empty, falls back to Selenium.
    Note: parse_func(soup) should raise Exception or return None if data is missing.
    """
    # 1. Default use BeautifulSoup via httpx
    try:
        logger.info(f"Attempting httpx scrape for {url}")
        async with httpx.AsyncClient() as client:
            # Must hit homepage first to obtain required NSE Akamai cookies
            await client.get("https://www.nseindia.com", headers=HEADERS, timeout=15)
            
            resp = await client.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            
            # Identify native API JSON
            content_type = resp.headers.get("Content-Type", "")
            if "application/json" in content_type:
                logger.info("Url returned JSON natively. Bypassing BeautifulSoup.")
                return resp.json()
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            data = parse_func(soup)
            if data:
                return data
            raise Exception("Parsing returned empty data")
    except Exception as e:
        logger.warning(f"BeautifulSoup method failed for {url}: {e}. Falling back to ChromeDriver.")

    # 2. Fallback to ChromeDriver
    driver = None
    try:
        driver = get_selenium_driver()
        driver.get(url)
        # Give it some time to load JavaScript content
        import time
        time.sleep(6)
        
        # Check if the page rendering is actually a JSON dump (sometimes happens in Selenium on API endpoints)
        page_source = driver.page_source
        try:
            import json
            inner_text = driver.find_element("tag name", "body").text
            return json.loads(inner_text)
        except:
            pass

        soup = BeautifulSoup(page_source, 'html.parser')
        data = parse_func(soup)
        if data:
            return data
        else:
            return {"error": "Both BS4 and Selenium failed to render target data."}
    except Exception as e:
        logger.error(f"Selenium fallback failed for {url}: {e}")
        return {"error": f"Scraping failed entirely: {e}"}
    finally:
        if driver:
            driver.quit()
