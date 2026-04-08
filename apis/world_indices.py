from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/world-indices", tags=["world_indices"])
async def get_world_indices():
    return await serve_data("world_indices")
