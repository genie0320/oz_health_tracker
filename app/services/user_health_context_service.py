"""공통② 질병/복약/목표 조회 단일창구. T-LLM-2, T-GOAL-2, T-GUIDE-1, T-ADH-2가 사용."""

from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_health_context(db: AsyncSession, profile_id: int) -> dict:
    # TODO: 관련 repository 완성 후 실제 조회 로직 연결
    return {"conditions": [], "medications": [], "goals": [], "profile_id": profile_id}
