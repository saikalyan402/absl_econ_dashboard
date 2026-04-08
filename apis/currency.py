from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/currency", tags=["currency"])
async def get_currency():
    return await serve_data("currency")
