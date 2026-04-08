from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/nifty", tags=["nifty"])
async def get_nifty():
    return await serve_data("nifty")
