# from sqlalchemy import Column, String, DateTime
# from datetime import datetime, timezone
# from database import Base

# class ScrapedData(Base):
#     __tablename__ = "scraped_data"

#     data_key = Column(String, primary_key=True, index=True)
#     payload = Column(String, nullable=False)
#     last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


from sqlalchemy import Column, String, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
from database import Base

IST = ZoneInfo("Asia/Kolkata")

class ScrapedData(Base):
    __tablename__ = "scraped_data"

    data_key = Column(String, primary_key=True, index=True)
    payload = Column(String, nullable=False)
    last_updated = Column(
        DateTime,
        default=lambda: datetime.now(IST),
        onupdate=lambda: datetime.now(IST)
    )