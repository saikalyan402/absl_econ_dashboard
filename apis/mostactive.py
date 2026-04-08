from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/mostactive", tags=["mostactive"])
async def get_mostactive():
    return await serve_data("mostactive")
