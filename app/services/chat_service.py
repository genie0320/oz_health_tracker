"""T-LLM-2 (AI 챗봇 상담) — 실시간 스트리밍, AI/RAG 워커의 동기 엔드포인트를 호출."""
from app.repositories.chat_repository import ChatRepository


class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    # TODO: 유스케이스 메서드 구현
