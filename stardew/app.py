# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/1/29 10:33
# @Description   :
from typing import NoReturn

from fastapi import FastAPI

from stardew import api
from stardew.core import deps
from stardew.api.common import login_router
from stardew.api.system import system_router
from stardew.core.container import IocContainer


def create_app() -> FastAPI:
    app = FastAPI()
    register_router(app)
    init_container()
    return app


def register_router(app: FastAPI) -> NoReturn:
    app.include_router(router=login_router)
    app.include_router(router=system_router)


def init_container():
    """
    装配Ioc容器。所有用到@inject的包都需要进行装配
    关于如何装配容器，参考 https://python-dependency-injector.ets-labs.org/wiring.html#wiring
    :return:
    """
    container = IocContainer()
    container.wire(packages=[
        api,
        deps
    ])
