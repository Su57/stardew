# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/4 17:32
# @Description   :
import pytest
from httpx import AsyncClient

from stardew.runserver import app


@pytest.mark.asyncio
async def test_captcha():
	async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as client:
		response = await client.get("/captcha")
	assert response.status_code == 200
