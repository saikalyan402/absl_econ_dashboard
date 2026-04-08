from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/snapshot", tags=["snapshot"])
async def get_snapshot():
    return await serve_data("snapshot")
