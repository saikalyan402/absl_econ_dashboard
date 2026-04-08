from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
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
import apis.high_low_52weeks as high_low_52weeks
import apis.volume_gainers as volume_gainers
import apis.all_indices as all_indices
import apis.commodity as commodity
import apis.currency as currency
import apis.world_indices as world_indices


# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Economic Dashboard API", description="Live NSE Market Data")
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, 
        os.getenv("API_USERNAME", "admin")
    )
    correct_password = secrets.compare_digest(
        credentials.password, 
        os.getenv("API_PASSWORD", "admin")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Mount routers with authentication dependency
app.include_router(nifty.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(mostactive.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(sme.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(securities.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(snapshot.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(high_low_52weeks.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(volume_gainers.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(all_indices.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(commodity.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(currency.router, prefix="/api", dependencies=[Depends(authenticate)])
app.include_router(world_indices.router, prefix="/api", dependencies=[Depends(authenticate)])




@app.get("/")
def home():
    return {"message": "Welcome to the Economic Dashboard. Go to /docs for Swagger UI"}
