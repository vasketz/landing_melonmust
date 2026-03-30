from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String)
    last_name = Column(String)

    email_encrypted = Column(String)
    phone_encrypted = Column(String)

    amount = Column(Integer)
    business = Column(String)

    score = Column(Integer)
    status = Column(String, default="new")

    create_at = Column(DateTime, default=datetime.utcnow)

    