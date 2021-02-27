# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/26 15:38
# @Description   :
from typing import AsyncIterator

from aioredis import create_redis_pool, Redis


async def init_redis_pool(redis_dsn: str) -> AsyncIterator[Redis]:
    pool = await create_redis_pool(redis_dsn)
    try:
        yield pool
    finally:
        pool.close()
        await pool.wait_closed()