"""
실제 LLM 스트리밍 호출. 2026-07: 비용 이유로 Claude 대신 OpenAI 저비용 모델을 사용한다
(decision_log.md 참고). 모델명은 `.env`의 OPENAI_MODEL 하나만 바꾸면 교체된다.
"""

from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.core.config import settings

_client: AsyncOpenAI | None = None

_SYSTEM_PROMPT = (
    "당신은 복약/건강관리 앱 ReMedi의 상담 도우미입니다. "
    "의학적 진단을 내리지 말고, 아래 참고 정보를 바탕으로 일반적인 안내만 제공하세요."
)


def _get_client() -> AsyncOpenAI:
    # 지연 생성: import 시점에 API 키가 없어도(테스트/CI) 이 모듈을 문제없이 import할 수 있어야 한다.
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


async def stream_reply(message: str, context: dict, chunks: list[str]) -> AsyncIterator[str]:
    context_text = "\n".join(chunks) if chunks else "관련 참고 문서가 아직 없습니다."
    stream = await _get_client().chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"{_SYSTEM_PROMPT}\n\n참고 정보:\n{context_text}"},
            {"role": "user", "content": message},
        ],
        stream=True,
    )
    async for event in stream:
        delta = event.choices[0].delta.content
        if delta:
            yield delta
