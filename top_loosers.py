from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/top_loosers", tags=["top_loosers"])
async def get_top_loosers():
    return await serve_data("top_loosers")
