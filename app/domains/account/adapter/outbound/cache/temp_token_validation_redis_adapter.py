from typing import Optional

import redis.asyncio as aioredis

from app.domains.account.application.port.temp_token_validation_port import TempTokenValidationPort

TEMP_TOKEN_PREFIX = "temp_token:"


class TempTokenValidationRedisAdapter(TempTokenValidationPort):

    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def get(self, token: str) -> Optional[str]:
        key = f"{TEMP_TOKEN_PREFIX}{token}"
        return await self._redis.get(key)

    async def delete(self, token: str) -> None:
        key = f"{TEMP_TOKEN_PREFIX}{token}"
        await self._redis.delete(key)
