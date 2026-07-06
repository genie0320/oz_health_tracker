"""DB 접근 전담. Service만 이 파일을 호출한다 (CODING_RULES.md 1번 — 계층 분리, 폴더 구조와 무관하게 유지)."""

from sqlalchemy.ext.asyncio import AsyncSession


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # TODO: CRUD 메서드 구현
