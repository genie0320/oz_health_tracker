from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # TODO: CRUD 메서드 구현
