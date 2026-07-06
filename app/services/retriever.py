"""
RAG Retriever 자리. AI/RAG 추론은 이 백엔드 프로세스에 두지 않는다
(decision_log.md "AI/RAG 워커 분리 원칙"). 실제로는 `ai_worker/sync_api.py`의
POST /retrieve를 호출해야 하지만, RAG(서현) 완성 전까지는 stub으로 둔다
(decision_log.md RAG Tier 구조 — T-LLM-2는 "실시간 필수" 항목).

⚠ RAG 완성 후 교체 방법 (ChatService 내부만 바뀌고 Router/DTO는 그대로):

    chunks = Retriever().search(message, context)
    ↓ 이렇게 교체
    resp = await httpx.AsyncClient().post(
        f"{settings.AI_WORKER_SYNC_URL}/retrieve", json={"query": message, "profile_id": profile_id}
    )
    chunks = resp.json()["chunks"]
"""


class Retriever:
    def search(self, query: str, context: dict) -> list[str]:
        return []
