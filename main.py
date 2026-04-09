from fastapi import FastAPI, Depends, HTTPException, status
import secrets
import os
from dotenv import load_dotenv
from database import engine, Base

load_dotenv()

import apis.nifty as nifty
import apis.mostactive as mostactive
import apis.sme as sme
import apis.securities as securities
import apis.snapshot as snapshot
import apis.volume_gainers as volume_gainers
import apis.all_indices as all_indices
import apis.commodity as commodity
import apis.currency as currency
import apis.world_indices as world_indices
import apis.economic_indicators as economic_indicators
import apis.high_52weeks as high_52weeks
import apis.low_52weeks as low_52weeks
# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Economic Dashboard API", description="Live NSE Market Data")

# Mount routers with authentication dependency
app.include_router(nifty.router, prefix="/api")
app.include_router(mostactive.router, prefix="/api")
app.include_router(sme.router, prefix="/api")
app.include_router(securities.router, prefix="/api")
app.include_router(snapshot.router, prefix="/api")
app.include_router(volume_gainers.router, prefix="/api")
app.include_router(all_indices.router, prefix="/api")
app.include_router(commodity.router, prefix="/api")
app.include_router(currency.router, prefix="/api")
app.include_router(world_indices.router, prefix="/api")
app.include_router(economic_indicators.router, prefix="/api")
app.include_router(low_52weeks.router, prefix="/api")
app.include_router(high_52weeks.router, prefix="/api")





@app.get("/")
def home():
    return {"message": "Welcome to the Economic Dashboard. Go to /docs for Swagger UI"}
