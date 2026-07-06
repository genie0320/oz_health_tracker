"""
[AUTH] User 테이블.
⚠ profile_id vs user_id: 아직 팀 결정 필요 (CODING_RULES.md 2-1 참고).
가족구성원관리(T-AUTH-6) 도입 전까지 결론 나야 함.
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
