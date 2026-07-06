"""
Router 레이어 규칙: HTTP 처리만, 판단 없음. T-LLM-2.
api_spec_core_v1.yaml의 /chat/sessions, /chat/sessions/{session_id}/messages 구현.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.dtos.chat import ChatMessageRequest, ChatSessionCreateResult
from app.repositories.chat_repository import ChatRepository
from app.services.chat_service import ChatService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(ChatRepository(db))


def _profile_id(user: dict) -> int:
    return int(user["sub"])


@router.post("/sessions", response_model=ChatSessionCreateResult, status_code=status.HTTP_201_CREATED)
async def create_session(
    user: dict = Depends(get_current_user),
    service: ChatService = Depends(get_service),
) -> ChatSessionCreateResult:
    session_id = await service.create_session(profile_id=_profile_id(user))
    return ChatSessionCreateResult(session_id=session_id)


@router.get("/sessions/{session_id}/messages")
async def get_history(
    session_id: str,
    user: dict = Depends(get_current_user),
    service: ChatService = Depends(get_service),
) -> list[dict]:
    session = await service.get_authorized_session(session_id, _profile_id(user))
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세션을 찾을 수 없습니다.")
    return await service.get_history(session.id)


@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: str,
    body: ChatMessageRequest,
    user: dict = Depends(get_current_user),
    service: ChatService = Depends(get_service),
) -> StreamingResponse:
    session = await service.get_authorized_session(session_id, _profile_id(user))
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세션을 찾을 수 없습니다.")

    return StreamingResponse(
        service.stream_message(session.id, _profile_id(user), body.message),
        media_type="text/plain",
    )
