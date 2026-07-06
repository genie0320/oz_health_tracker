"""API 엔드포인트. Service만 호출하고, 여기서 비즈니스 판단을 하지 않는다."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.utils.security import create_access_token

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(AuthRepository(db))


@router.get("/ping")
async def ping():
    return {"domain": "auth", "status": "scaffold-ok"}


if settings.ENV == "local":
    # 실제 로그인(T-AUTH-1~4)이 아직 구현되지 않아, 다른 기능(T-LLM-2 등)을 로컬에서 테스트하려면
    # 토큰이 필요하다. `ENV=local`에서만 활성화되므로 배포 환경에는 존재하지 않는다.
    # 실제 로그인이 구현되면 이 엔드포인트는 삭제한다.
    @router.get("/dev/token")
    async def dev_token() -> dict:
        return {"token": create_access_token("1")}
