from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/commodity", tags=["commodity"])
async def get_commodity():
    return await serve_data("commodity")
