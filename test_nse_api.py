import asyncio
import httpx
from bs4 import BeautifulSoup
import json

async def test():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }

    async with httpx.AsyncClient() as client:
        r1 = await client.get("https://www.nseindia.com", headers=HEADERS, timeout=15)
        print("Got cookies")
        
        urls = [
            "https://www.nseindia.com/api/live-analysis-52Week?index=high",
            "https://www.nseindia.com/api/live-analysis-volume-gainers",
            "https://www.nseindia.com/api/live-analysis-most-active-securities?index=volume"
        ]
        
        for url in urls:
            r2 = await client.get(url, headers=HEADERS, timeout=15)
            print(f"{url} -> {r2.status_code}")
            try:
                print(str(r2.json())[:100])
            except:
                print("Not JSON")

asyncio.run(test())
