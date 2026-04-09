from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.get("/economic-indicators", tags=["economic_indicators"])
def get_economic_indicators(db: Session = Depends(get_db)):
    try:
        # Fetching data using raw SQL since dynamic table might not have an ORM model
        query = text('SELECT "Economic indicators" AS indicator, "value", "percentage" FROM economic_indicators')
        result = db.execute(query).fetchall()
        
        # Formatting as a key-value pair 
        # data = {row[0]: {"value": row[1], "percentage": row[2]} for row in result}
        # Formatting as an array of objects
        data = [
            {
                "indicator": row[0], 
                "value": row[1], 
                "percentage": row[2]
            } for row in result
        ]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
