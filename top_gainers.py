from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/top_gainers", tags=["top_gainers"])
async def get_top_gainers():
    return await serve_data("top_gainers")
