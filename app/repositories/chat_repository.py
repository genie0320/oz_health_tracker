"""DB 접근 전담. Service만 이 파일을 호출한다 (CODING_RULES.md 1번)."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatMessage, ChatSession


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, profile_id: int) -> ChatSession:
        session = ChatSession(profile_id=profile_id, session_uuid=str(uuid.uuid4()))
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session_by_uuid(self, session_uuid: str) -> ChatSession | None:
        result = await self.db.execute(select(ChatSession).where(ChatSession.session_uuid == session_uuid))
        return result.scalar_one_or_none()

    async def save_message(self, session_id: int, profile_id: int, role: str, content: str) -> None:
        self.db.add(ChatMessage(session_id=session_id, profile_id=profile_id, role=role, content=content))
        await self.db.commit()

    async def history_for(self, session_id: int) -> list[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)
        )
        return list(result.scalars().all())
