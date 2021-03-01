# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/1/29 11:55
# @Description   : 统一装配所有router
from fastapi import APIRouter

from stardew.api.system import system_router
from stardew.api.common import login_router

api = APIRouter()

api.include_router(router=system_router, prefix='/sys')
api.include_router(router=login_router)
