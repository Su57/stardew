# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/8 12:38
# @Description   :

from fastapi import APIRouter

from .user_controller import user_router


system_router = APIRouter(prefix="/system")

system_router.include_router(router=user_router, prefix="/user")


__all__ = {
    "system_router"
}
