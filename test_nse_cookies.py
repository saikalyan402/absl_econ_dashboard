import asyncio
import httpx
from bs4 import BeautifulSoup
from scraper_jobs import URLS

async def test():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }

    async with httpx.AsyncClient() as client:
        print("Fetching main page for cookies...")
        r1 = await client.get("https://www.nseindia.com", headers=HEADERS, timeout=15)
        print("Cookies:", dict(client.cookies))
        
        url = URLS["high_low_52weeks"]
        print(f"Fetching {url}")
        r2 = await client.get(url, headers=HEADERS, timeout=15)
        print(f"Status: {r2.status_code}")
        soup = BeautifulSoup(r2.text, 'html.parser')
        tables = soup.find_all("table")
        print(f"BS4 found {len(tables)} tables")

asyncio.run(test())
