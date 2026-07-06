"""API 엔드포인트. Service만 호출하고, 여기서 비즈니스 판단을 하지 않는다."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(AuthRepository(db))


@router.get("/ping")
async def ping():
    return {"domain": "auth", "status": "scaffold-ok"}
