import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, nullable=False, index=True)  # user_id 아님 — CODING_RULES.md 2-1
    drug_name = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
