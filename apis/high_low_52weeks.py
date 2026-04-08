from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/high_low_52weeks", tags=["high_low_52weeks"])
async def get_high_low_52weeks():
    return await serve_data("high_low_52weeks")
