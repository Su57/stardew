# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/8 12:38
# @Description   : 系统路由装配

from fastapi import APIRouter

from .user_controller import user_router
from .role_controller import role_router
from .menu_controller import menu_router


system_router = APIRouter()

system_router.include_router(router=user_router, prefix="/user")
system_router.include_router(router=role_router, prefix="/role")
system_router.include_router(router=menu_router, prefix="/menu")


__all__ = {
    "system_router",
}
