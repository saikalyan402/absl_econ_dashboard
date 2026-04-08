from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/securities", tags=["securities"])
async def get_securities():
    return await serve_data("securities")
