from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/volume_gainers", tags=["volume_gainers"])
async def get_volume_gainers():
    return await serve_data("volume_gainers")
