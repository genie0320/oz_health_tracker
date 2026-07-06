"""
Redis Streams 컨슈머 — 알림 발송 등 AI/RAG가 아닌 백그라운드 작업.
(AI/RAG/멀티모달 관련 워커는 여기가 아니라 scaffold/ai_worker/에 있다 — decision_log.md 참고)
"""

import asyncio

from app.core.database import get_redis


async def consume_push_notifications():
    redis = get_redis()
    last_id = "0"
    while True:
        results = await redis.xread({"notifications:push": last_id}, block=5000, count=10)
        for _stream, messages in results:
            for message_id, data in messages:
                last_id = message_id
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(consume_push_notifications())
