"""T-LLM-3(건강 콘텐츠 생성 파이프라인) — APScheduler 새벽 배치에서 호출될 자리."""


async def generate_content(condition_tag: str) -> dict:
    raise NotImplementedError("RAG 완성 후 구현")
