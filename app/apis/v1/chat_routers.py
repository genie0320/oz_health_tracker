from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.chat_repository import ChatRepository
from app.services.chat_service import ChatService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(ChatRepository(db))


@router.get("/ping")
async def ping():
    return {"domain": "chat", "status": "scaffold-ok"}
