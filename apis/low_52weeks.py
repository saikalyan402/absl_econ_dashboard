from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/low_52weeks", tags=["low_52weeks"])
async def get_low_52weeks():
    return await serve_data("low_52weeks")
