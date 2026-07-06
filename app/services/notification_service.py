"""공통④ Push 발송. 실제 발송은 app/workers/의 Redis Streams 컨슈머가 처리."""
from redis.asyncio import Redis


async def enqueue_push_notification(redis: Redis, user_id: int, title: str, body: str) -> None:
    await redis.xadd("notifications:push", {"user_id": user_id, "title": title, "body": body})
