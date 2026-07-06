"""
job 등록 후 폴링해도 되는 작업 전용 — Redis Streams 컨슈머.
T-MED-1/T-DOC-1(인식), T-LLM-3(콘텐츠 생성) 등.
"""

import asyncio

from redis.asyncio import Redis

from ai_worker.core.config import settings


async def consume_recognition_jobs():
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
    last_id = "0"
    while True:
        results = await redis.xread({"recognition:jobs": last_id}, block=5000, count=10)
        for _stream, messages in results:
            for message_id, data in messages:
                # TODO: ai_worker/tasks/recognition_task.py 호출
                last_id = message_id
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(consume_recognition_jobs())
