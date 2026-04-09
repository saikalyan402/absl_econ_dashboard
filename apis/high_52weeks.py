from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/high_52weeks", tags=["high_52weeks"])
async def get_high_52weeks():
    return await serve_data("high_52weeks")
