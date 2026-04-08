import json
import asyncio
from typing import Optional
from fastapi import HTTPException
from scraper_core import fetch_with_bs4_and_fallback
from database import SessionLocal
from models import ScrapedData

URLS = {
    "nifty": "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050",
    "mostactive": "https://www.nseindia.com/api/live-analysis-most-active-securities?index=volume",
    "sme": "https://www.nseindia.com/api/liveAnalysis-sme?index=sme",
    "securities": "https://www.nseindia.com/api/pre-open-market-cm-and-emerge-market",
    "snapshot": "https://www.nseindia.com/api/marketStatus",
    "high_low_52weeks": "https://www.nseindia.com/api/live-analysis-52Week?index=high",
    "volume_gainers": "https://www.nseindia.com/api/live-analysis-volume-gainers",
    "all_indices": "https://www.nseindia.com/api/allIndices",
    "commodity": "https://www.nseindia.com/api/NextApi/apiClient?functionName=getReferenceRates&&type=null&&flag=CSR",
    "currency": "https://www.nseindia.com/api/NextApi/apiClient?functionName=getReferenceRates&&type=null&&flag=CUR",
    "world_indices": "https://finance.yahoo.com/markets/world-indices/"

}

# def generic_table_parser(soup):
#     tables = soup.find_all("table")
#     if not tables:
#         return None
#     data = []
    
#     # Grab the largest active table on the page
#     table = max(tables, key=lambda t: len(t.find_all('tr')))
#     rows = table.find_all("tr")
#     if not rows:
#         return None
        
#     headers = [th.text.strip() for th in rows[0].find_all(["th", "td"])]
#     if not headers:
#         return None
        
#     for row in rows[1:]:
#         cols = [td.text.strip() for td in row.find_all(["td", "th"])]
#         if len(cols) == len(headers):
#             data.append(dict(zip(headers, cols)))
#     return data if data else None

# async def fetch_and_store(key: str, url: str):
#     # This invokes BS4 -> Selenium fallback chain from scraper_core
#     data = await fetch_with_bs4_and_fallback(url, generic_table_parser)
    
#     # Check if a valid payload was returned, not our error dict wrapper
#     if isinstance(data, list) or (isinstance(data, dict) and "error" not in data):
#         db = SessionLocal()
#         try:
#             record = db.query(ScrapedData).filter(ScrapedData.data_key == key).first()
#             payload_str = json.dumps(data)
#             if record:
#                 record.payload = payload_str
#             else:
#                 new_record = ScrapedData(data_key=key, payload=payload_str)
#                 db.add(new_record)
#             db.commit()
#         finally:
#             db.close()
#         return data
#     else:
#         # Return the error wrapper directly
#         return data

# async def serve_data(key: str):
#     db = SessionLocal()
#     try:
#         record = db.query(ScrapedData).filter(ScrapedData.data_key == key).first()
#     finally:
#         db.close()
    
#     url = URLS.get(key)
#     if not url:
#         raise HTTPException(status_code=404, detail="Requested URL configuration not found.")
    
#     # Stale-While-Revalidate pattern for robustness
#     if record:
#         # Serve the cached database JSON instantly
#         cached_result = json.loads(record.payload)
        
#         # Trigger background scrape continuously to update database silently without blocking the user
#         asyncio.create_task(fetch_and_store(key, url))
#         return cached_result
#     else:
#         # We don't have historical data. We MUST block and wait for the scrape.
#         # This guarantees first-time users see either the fresh data or the definitive error response.
#         result = await fetch_and_store(key, url)
        
#         # If the result happens to be an error dict from our fallback inside scraper_core.py
#         if isinstance(result, dict) and "error" in result:
#             raise HTTPException(
#                 status_code=503, 
#                 detail=f"Scraping Engine failed to fetch data: {result['error']}"
#             )
#         elif not result:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Scraping Engine returned empty data. The table might be missing or the NSE DOM layout changed."
#             )
            
#         return result


def generic_table_parser(soup):
    tables = soup.find_all("table")
    if not tables:
        return None
    data = []
    
    # Grab the largest active table on the page
    table = max(tables, key=lambda t: len(t.find_all('tr')))
    rows = table.find_all("tr")
    if not rows:
        return None
        
    import re
    headers = [re.sub(r'\s+', ' ', th.text.strip()) for th in rows[0].find_all(["th", "td"])]
    if not headers:
        return None
        
    for row in rows[1:]:
        cols = [re.sub(r'\s+', ' ', td.text.strip()) for td in row.find_all(["td", "th"])]
        if len(cols) == len(headers):
            data.append(dict(zip(headers, cols)))
    return data if data else None

async def fetch_and_store(key: str, url: str):
    # This invokes BS4 -> Selenium fallback chain from scraper_core
    data = await fetch_with_bs4_and_fallback(url, generic_table_parser)
    
    # Check if a valid payload was returned, not our error dict wrapper
    if isinstance(data, list) or (isinstance(data, dict) and "error" not in data):
        db = SessionLocal()
        try:
            record = db.query(ScrapedData).filter(ScrapedData.data_key == key).first()
            payload_str = json.dumps(data)
            if record:
                record.payload = payload_str
            else:
                new_record = ScrapedData(data_key=key, payload=payload_str)
                db.add(new_record)
            db.commit()
        finally:
            db.close()
        return data
    else:
        # Return the error wrapper directly
        return data

async def serve_data(key: str):
    db = SessionLocal()
    try:
        record = db.query(ScrapedData).filter(ScrapedData.data_key == key).first()
    finally:
        db.close()
    
    url = URLS.get(key)
    if not url:
        raise HTTPException(status_code=404, detail="Requested URL configuration not found.")
    
    # Stale-While-Revalidate pattern for robustness
    if record:
        # Serve the cached database JSON instantly
        cached_result = json.loads(record.payload)
        
        # Trigger background scrape continuously to update database silently without blocking the user
        asyncio.create_task(fetch_and_store(key, url))
        return cached_result
    else:
        # We don't have historical data. We MUST block and wait for the scrape.
        # This guarantees first-time users see either the fresh data or the definitive error response.
        result = await fetch_and_store(key, url)
        
        # If the result happens to be an error dict from our fallback inside scraper_core.py
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(
                status_code=503, 
                detail=f"Scraping Engine failed to fetch data: {result['error']}"
            )
        elif not result:
            raise HTTPException(
                status_code=500,
                detail="Scraping Engine returned empty data. The table might be missing or the NSE DOM layout changed."
            )
            
        return result
