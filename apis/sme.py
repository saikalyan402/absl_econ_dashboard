from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/sme", tags=["sme"])
async def get_sme():
    return await serve_data("sme")
