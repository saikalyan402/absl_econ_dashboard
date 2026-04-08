from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/all_indices", tags=["all_indices"])
async def get_all_indices():
    return await serve_data("all_indices")
